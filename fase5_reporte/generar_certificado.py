#!/usr/bin/env python3
import os
import yaml
from datetime import datetime

# Cargar variables
with open("../vars/vars_001V-11.yaml", "r") as f:
    vars = yaml.safe_load(f)

alumno  = vars["alumno"]
cliente = vars["cliente"]
router  = vars["router"]

# Verificar resultados de fases anteriores
def check_conforme(archivo):
    try:
        with open(archivo, "r") as f:
            contenido = f.read()
            return "RESULTADO GLOBAL: CONFORME" in contenido
    except:
        return False

netconf_ok  = check_conforme("../fase3_validacion_netconf/evidencias/output_validacion_netconf.txt")
restconf_ok = check_conforme("../fase4_validacion_restconf/evidencias/output_validacion_restconf.txt")

# Verificar diff
diff_dir = "evidencias/diff_001V-11"
diff_ok  = os.path.exists(diff_dir) and len(os.listdir(diff_dir)) > 0

resultado_global = "CONFORME" if (netconf_ok and restconf_ok and diff_ok) else "NO CONFORME"

# Generar certificado
certificado = f"""
================================================================================
         CERTIFICADO DE COMPLIANCE — IMPLEMENTACION DE RED
================================================================================
Fecha de emision  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
--------------------------------------------------------------------------------
DATOS DEL ALUMNO
  Codigo          : {alumno['codigo']}
  Nombre          : {alumno['nombre']}
--------------------------------------------------------------------------------
DATOS DEL CLIENTE
  Empresa         : {cliente['empresa']}
  Hostname        : {cliente['hostname']}
  Router IP       : {router['ip']}
--------------------------------------------------------------------------------
CONFIGURACION APLICADA
  Hostname        : {cliente['hostname']}
  Loopback IP     : {router['loopback_ip']}/{router['loopback_prefix']}
  Descripcion WAN : {router['descripcion_wan']}
  Servidor NTP    : {router['ntp_server']}
  Banner          : {router['banner']}
--------------------------------------------------------------------------------
RESULTADOS DE VALIDACION
  NETCONF  (5/5 criterios) : {"CONFORME" if netconf_ok  else "NO CONFORME"}
  RESTCONF (4/4 criterios) : {"CONFORME" if restconf_ok else "NO CONFORME"}
  Diff baseline vs final   : {"CONFORME" if diff_ok     else "NO CONFORME"}
--------------------------------------------------------------------------------
RESULTADO GLOBAL           : {resultado_global}
--------------------------------------------------------------------------------
El equipo ha sido configurado, validado y auditado exitosamente.
Listo para operacion en red corporativa de {cliente['empresa']}.
================================================================================
"""

print(certificado)

# Guardar certificado
with open(f"evidencias/certificado_compliance_001V-11.txt", "w") as f:
    f.write(certificado)

print("Certificado guardado en evidencias/certificado_compliance_001V-11.txt")
