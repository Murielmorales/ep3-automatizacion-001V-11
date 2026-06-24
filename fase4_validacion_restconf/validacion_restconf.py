#!/usr/bin/env python3
import sys
import json
import yaml
import requests
from datetime import datetime

requests.packages.urllib3.disable_warnings()

print("=" * 60)
print("Script  : validacion_restconf.py")
print(f"Fecha   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Host VM : labvm")
print("=" * 60)

with open("../vars/vars_001V-11.yaml", "r") as f:
    vars = yaml.safe_load(f)

alumno  = vars["alumno"]
cliente = vars["cliente"]
router  = vars["router"]

print(f"Alumno  : {alumno['codigo']} - {alumno['nombre']}")
print(f"Empresa : {cliente['empresa']}")
print("=" * 60)

BASE_URL = f"https://{router['ip']}/restconf/data"
HEADERS  = {"Accept": "application/yang-data+json"}
AUTH     = (router["usuario"], router["password"])

def consultar(endpoint, archivo):
    url = f"{BASE_URL}/{endpoint}"
    resp = requests.get(url, headers=HEADERS, auth=AUTH, verify=False)
    datos = resp.json()
    with open(f"evidencias/responses/{archivo}", "w") as f:
        json.dump(datos, f, indent=2)
    print(f"Guardado: evidencias/responses/{archivo}")
    return datos

print("\nConsultando endpoints RESTCONF...\n")

hostname_data   = consultar("Cisco-IOS-XE-native:native/hostname", "get_hostname.json")
loopback_data   = consultar(f"ietf-interfaces:interfaces/interface=Loopback{router['loopback_id']}", "get_loopback.json")
interfaces_data = consultar("ietf-interfaces:interfaces/interface=GigabitEthernet1", "get_interfaces.json")
ntp_data        = consultar("Cisco-IOS-XE-native:native/ntp", "get_ntp.json")

# Extraer valores con estructura correcta
hostname_actual = hostname_data.get("Cisco-IOS-XE-native:hostname", "NO ENCONTRADO")

loopback_actual = "NO ENCONTRADO"
try:
    loopback_actual = loopback_data["ietf-interfaces:interface"]["ietf-ip:ipv4"]["address"][0]["ip"]
except:
    pass

desc_actual = "NO ENCONTRADO"
try:
    desc_actual = interfaces_data["ietf-interfaces:interface"]["description"]
except:
    pass

ntp_actual = "NO ENCONTRADO"
try:
    ntp_actual = ntp_data["Cisco-IOS-XE-native:ntp"]["Cisco-IOS-XE-ntp:server"]["server-list"][0]["ip-address"]
except:
    pass

print("\n--- REPORTE DE VALIDACION RESTCONF ---\n")
resultados = []

def verificar(criterio, esperado, obtenido):
    ok = esperado == obtenido
    estado = "[OK]" if ok else "[FAIL]"
    print(f"{estado} {criterio}")
    print(f"      Esperado : {esperado}")
    print(f"      Obtenido : {obtenido}")
    resultados.append(ok)

verificar("Hostname corporativo", cliente["hostname"],       hostname_actual)
verificar("IP Loopback",          router["loopback_ip"],     loopback_actual)
verificar("Descripcion WAN",      router["descripcion_wan"], desc_actual)
verificar("Servidor NTP",         router["ntp_server"],      ntp_actual)

total    = len(resultados)
ok_count = sum(resultados)
print(f"\nResultado: {ok_count}/{total} criterios conformes")

if ok_count == total:
    print("\n✅ RESULTADO GLOBAL: CONFORME")
else:
    print("\n❌ RESULTADO GLOBAL: NO CONFORME")
