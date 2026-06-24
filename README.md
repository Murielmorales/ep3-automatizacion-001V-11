# EP3 — Implementación de Automatización de Red

## 1. Objetivo del proyecto
Incorporar el router RTR-NAVPAC a la red corporativa de Naviera del Pacifico SA mediante un ciclo completo de automatización, aplicando configuración estándar de forma reproducible y verificando su correcta implementación con herramientas de gestión de red.

## 2. Alcance
Se configuró hostname, banner, NTP, interfaz WAN y Loopback de gestión. Se habilitaron NETCONF y RESTCONF. No se abordó configuración de routing dinámico ni seguridad avanzada. Las herramientas utilizadas fueron pyATS/Genie, Ansible, ncclient y requests.

## 3. Infraestructura utilizada
| Componente | Detalle |
|-----------|---------|
| Router | Cisco CSR1000v — IOS-XE 16.9.5 |
| IP Router | 192.168.56.113 |
| Estación de trabajo | DEVASC VM (Ubuntu, devasc@labvm) |
| Python | 3.8.2 |
| Ansible | 2.9.9 |
| pyATS/Genie | 20.5 |

## 4. Tecnologías empleadas y justificación
- **pyATS/Genie**: Usado en Fase 1 y 5 para capturar el estado del router vía SSH y comparar cambios, sin requerir NETCONF habilitado previamente.
- **Ansible**: Usado en Fase 2 para aplicar la configuración corporativa de forma idempotente y reproducible mediante playbooks declarativos.
- **NETCONF**: Usado en Fase 3 para validar la configuración mediante consultas al árbol XML completo del dispositivo, de forma independiente a Ansible.
- **RESTCONF**: Usado en Fase 4 para verificar recursos específicos del router en formato JSON mediante URLs, complementando la validación NETCONF.

## 5. Configuración aplicada
| Parámetro | Valor |
|-----------|-------|
| Hostname | RTR-NAVPAC |
| Loopback IP | 10.1.11.1/24 |
| Descripción WAN | Enlace-WAN-Arica |
| Servidor NTP | 9.9.9.9 |
| Banner | ACCESO RESTRINGIDO - NAVPAC |
| NETCONF | Habilitado (puerto 830) |
| RESTCONF | Habilitado (HTTPS) |

## 6. Resultados de validación
| Criterio | NETCONF | RESTCONF |
|---------|---------|----------|
| Hostname corporativo | CONFORME | CONFORME |
| IP Loopback | CONFORME | CONFORME |
| Máscara Loopback | CONFORME | — |
| Descripción WAN | CONFORME | CONFORME |
| Servidor NTP | CONFORME | CONFORME |
| **Resultado global** | **CONFORME** | **CONFORME** |

## 7. Conclusiones
El router RTR-NAVPAC fue configurado, validado y auditado exitosamente. Todos los criterios de compliance resultaron CONFORME mediante validación independiente con NETCONF y RESTCONF. El equipo queda listo para operar en la red corporativa de Naviera del Pacifico SA. El proceso quedó completamente documentado y auditado en este repositorio GitHub.

---
**Alumno:** Constanza Morales | **Código:** 001V-11 | **Empresa:** Naviera del Pacifico SA
