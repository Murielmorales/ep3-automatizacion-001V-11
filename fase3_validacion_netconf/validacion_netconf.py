#!/usr/bin/env python3
import sys
import yaml
from datetime import datetime
from ncclient import manager
from xml.etree import ElementTree as ET

# Metadatos
print("=" * 60)
print("Script  : validacion_netconf.py")
print(f"Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Host VM : labvm")
print("=" * 60)

# Cargar variables
with open("../vars/vars_001V-11.yaml", "r") as f:
    vars = yaml.safe_load(f)

alumno  = vars["alumno"]
cliente = vars["cliente"]
router  = vars["router"]

print(f"Alumno  : {alumno['codigo']} - {alumno['nombre']}")
print(f"Empresa : {cliente['empresa']}")
print("=" * 60)

# Filtro NETCONF
filtro_xml = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>
    <interface>
      <Loopback/>
      <GigabitEthernet/>
    </interface>
    <ntp/>
  </native>
</filter>
"""

# Conectar via NETCONF
print("\nConectando al router via NETCONF...")
try:
    with manager.connect(
        host=router["ip"],
        port=830,
        username=router["usuario"],
        password=router["password"],
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False
    ) as m:
        respuesta = m.get_config(source="running", filter=filtro_xml)
        xml_crudo = respuesta.xml

        with open("evidencias/rpc_reply_raw.xml", "w") as f:
            f.write(xml_crudo)
        print("XML guardado en evidencias/rpc_reply_raw.xml")

        # Buscar NTP en el XML completo
        root = ET.fromstring(xml_crudo)
        xml_str = xml_crudo

        ns = {
            "ios": "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
            "ntp": "http://cisco.com/ns/yang/Cisco-IOS-XE-ntp"
        }

        hostname_elem = root.find(".//ios:native/ios:hostname", ns)
        hostname_actual = hostname_elem.text if hostname_elem is not None else "NO ENCONTRADO"

        loopback_ip_elem = root.find(".//ios:native/ios:interface/ios:Loopback/ios:ip/ios:address/ios:primary/ios:address", ns)
        loopback_ip_actual = loopback_ip_elem.text if loopback_ip_elem is not None else "NO ENCONTRADO"

        loopback_mask_elem = root.find(".//ios:native/ios:interface/ios:Loopback/ios:ip/ios:address/ios:primary/ios:mask", ns)
        loopback_mask_actual = loopback_mask_elem.text if loopback_mask_elem is not None else "NO ENCONTRADO"

        desc_elem = root.find(".//ios:native/ios:interface/ios:GigabitEthernet/ios:description", ns)
        desc_actual = desc_elem.text if desc_elem is not None else "NO ENCONTRADO"

        # Buscar NTP con diferentes namespaces posibles
        ntp_actual = "NO ENCONTRADO"
        for elem in root.iter():
            if elem.tag.endswith("}ip") or elem.tag == "ip":
                parent = elem.tag
                # verificar si el padre es server-list
                if router["ntp_server"] in (elem.text or ""):
                    ntp_actual = elem.text
                    break
            if "server-list" in elem.tag or "server" in elem.tag:
                for child in elem:
                    if child.text and router["ntp_server"] in child.text:
                        ntp_actual = child.text
                        break

        # Si aún no encontrado, buscar en texto crudo
        if ntp_actual == "NO ENCONTRADO" and router["ntp_server"] in xml_str:
            ntp_actual = router["ntp_server"]

        print("\n--- REPORTE DE VALIDACION NETCONF ---\n")
        resultados = []

        def verificar(criterio, esperado, obtenido):
            ok = esperado == obtenido
            estado = "[OK]" if ok else "[FAIL]"
            print(f"{estado} {criterio}")
            print(f"      Esperado : {esperado}")
            print(f"      Obtenido : {obtenido}")
            resultados.append(ok)

        verificar("Hostname corporativo",  cliente["hostname"],       hostname_actual)
        verificar("IP Loopback",           router["loopback_ip"],     loopback_ip_actual)
        verificar("Mascara Loopback",      router["loopback_mask"],   loopback_mask_actual)
        verificar("Descripcion WAN",       router["descripcion_wan"], desc_actual)
        verificar("Servidor NTP",          router["ntp_server"],      ntp_actual)

        total    = len(resultados)
        ok_count = sum(resultados)
        print(f"\nResultado: {ok_count}/{total} criterios conformes")

        if ok_count == total:
            print("\n✅ RESULTADO GLOBAL: CONFORME")
        else:
            print("\n❌ RESULTADO GLOBAL: NO CONFORME")

except Exception as e:
    print(f"ERROR al conectar: {e}")
    sys.exit(1)
