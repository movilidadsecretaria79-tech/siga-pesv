from django.core.management.base import BaseCommand
from pesv.models import PasoPESV, Componente, InstrumentoInspeccion


PASOS = [
    # numero, nombre, fase, nivel_aplicable
    (1, "Líder del diseño e implementación del PESV", 1, "TODOS"),
    (2, "Comité de Seguridad Vial (CSV)", 1, "ESTANDAR_AVANZADO"),
    (3, "Política de Seguridad Vial de la Organización", 1, "TODOS"),
    (4, "Liderazgo, compromiso y corresponsabilidad del nivel directivo", 1, "TODOS"),
    (5, "Diagnóstico", 1, "TODOS"),
    (6, "Caracterización, evaluación y control de riesgos", 1, "TODOS"),
    (7, "Objetivos y metas del PESV", 1, "TODOS"),
    (8, "Programas de gestión de riesgos críticos y factores de desempeño", 1, "TODOS"),
    (9, "Plan anual de trabajo", 2, "TODOS"),
    (10, "Competencia y plan anual de formación", 2, "TODOS"),
    (11, "Responsabilidad y comportamiento seguro", 2, "AVANZADO"),
    (12, "Plan de preparación y respuesta ante emergencias viales", 2, "TODOS"),
    (13, "Investigación interna de siniestros viales", 2, "ESTANDAR_AVANZADO"),
    (14, "Vías seguras administradas por la organización", 2, "TODOS"),
    (15, "Planificación de desplazamientos laborales", 2, "TODOS"),
    (16, "Inspección de vehículos y equipos", 2, "TODOS"),
    (17, "Mantenimiento y control de vehículos seguros y equipos", 2, "TODOS"),
    (18, "Gestión del cambio y gestión de contratistas", 2, "ESTANDAR_AVANZADO"),
    (19, "Archivo y retención documental", 2, "ESTANDAR_AVANZADO"),
    (20, "Indicadores y reporte de autogestión PESV", 3, "TODOS"),
    (21, "Registro y análisis estadístico de siniestros viales", 3, "AVANZADO"),
    (22, "Auditoría anual", 3, "TODOS"),
    (23, "Mejora continua, acciones preventivas y correctivas", 4, "TODOS"),
    (24, "Mecanismos de comunicación y participación", 4, "TODOS"),
]

# codigo, nombre, paso_principal, pregunta_verificacion, tipo_evidencia
COMPONENTES = [
    ("C01", "PESV vigente (documento marco)", 1,
     "¿La organización cuenta con un documento de PESV vigente, formalmente adoptado?", "AMBOS"),
    ("C02", "Designación del líder del PESV", 1,
     "¿Existe acta de designación del líder del PESV y este diligencia el reporte de autogestión anual y la medición de indicadores?", "AMBOS"),
    ("C03", "Comité de Seguridad Vial (CSV)", 2,
     "¿El nivel directivo designó los miembros del CSV? ¿Está conformado por al menos 3 personas con poder de decisión, incluido el líder del PESV? ¿Cumple con sus responsabilidades y funciones?", "AMBOS"),
    ("C04", "Política de Seguridad Vial", 3,
     "¿Se tiene la política de seguridad vial y cumple con los requisitos definidos en el Paso 3?", "AMBOS"),
    ("C05", "Liderazgo del nivel directivo", 4,
     "¿El nivel directivo demuestra liderazgo, compromiso y corresponsabilidad? ¿Se cumple con los requisitos definidos en el Paso 4?", "AMBOS"),
    ("C06", "Diagnóstico: caracterización de la población expuesta", 5,
     "Cantidad de sedes, servicios prestados, lista de contratistas, lista de colaboradores, rutas frecuentes, colaboradores capacitados en respuesta a emergencias viales, inventario de vehículos.", "AMBOS"),
    ("C07", "Caracterización del riesgo vial / Matriz de riesgos viales", 6,
     "¿Existe procedimiento y matriz de caracterización de riesgos viales que evalúe los riesgos?", "AMBOS"),
    ("C08", "Objetivos, metas e indicadores", 7,
     "¿Existen objetivos y metas del PESV, tienen indicadores definidos y seguimiento periódico?", "AMBOS"),
    ("C09", "Programas de gestión de riesgos críticos", 8,
     "¿Existen campañas de prevención y de uso de elementos de protección personal en marcha?", "AMBOS"),
    ("C10", "Plan anual de trabajo del PESV", 9,
     "¿La empresa cuenta con un plan anual de trabajo del PESV con actividades, responsables y fechas?", "AMBOS"),
    ("C11", "Competencias y plan anual de formación", 10,
     "Programa de capacitación en seguridad vial, inducción y re-inducción, evidencias de asistencia y evaluación.", "AMBOS"),
    ("C12", "Requisitos de contratación en materia de seguridad vial", 10,
     "¿Se documentan los requisitos de seguridad vial exigidos en los procesos de contratación?", "DOCUMENTO"),
    ("C13", "Funciones en materia de seguridad vial documentadas", 10,
     "¿Están documentadas las funciones y responsabilidades en seguridad vial de los distintos roles?", "DOCUMENTO"),
    ("C14", "Gestión de conductores: licencias, exámenes, comparendos, competencias, fatiga y reincidencia", 10,
     "Licencias de conducción vigentes, exámenes médicos ocupacionales, verificación de comparendos e infracciones, evaluación de competencias para la movilidad segura, control de jornadas laborales y fatiga, seguimiento a conductores reincidentes. (Ver módulo de Conductores por empresa.)", "AMBOS"),
    ("C15", "Plan de preparación y respuesta ante emergencias viales", 12,
     "Reporte de siniestros, cadena de llamado, riesgos de la ruta, número de llamado de emergencia, brigadistas capacitados, botiquines y equipos disponibles, simulacros realizados.", "AMBOS"),
    ("C16", "Procedimiento de investigación de siniestros viales", 13,
     "¿Existe procedimiento de investigación con análisis de causa raíz, lecciones aprendidas, acciones correctivas y seguimiento a las mismas?", "AMBOS"),
    ("C17", "Vías seguras administradas por la organización", 14,
     "¿Se identifican y gestionan los riesgos de las vías administradas directamente por la organización (si aplica)?", "AMBOS"),
    ("C18", "Planificación de desplazamientos laborales", 15,
     "¿Existe procedimiento y documentos de planificación de los desplazamientos laborales de los colaboradores?", "AMBOS"),
    ("C19", "Inspección de vehículos y equipos", 16,
     "Estado de los vehículos, condiciones de operación, evidencias de control a conductores, registros documentales, cumplimiento de procedimientos internos, SOAT vigente, revisión técnico-mecánica vigente, control de llantas y sistemas de seguridad.", "AMBOS"),
    ("C20", "Mantenimiento preventivo y correctivo de vehículos", 17,
     "¿Existe programa de mantenimiento preventivo de vehículos y equipos y registro de mantenimiento correctivo?", "AMBOS"),
    ("C21", "Gestión del cambio", 18,
     "¿Existe procedimiento para evaluar el impacto de cambios internos/externos (rutas, tecnologías, legislación, etc.) en la seguridad vial?", "DOCUMENTO"),
    ("C22", "Gestión de contratistas", 18,
     "¿Los contratistas están incluidos en el PESV? Verificación documental de vehículos contratados, seguimiento a conductores tercerizados, requisitos de seguridad vial en los contratos.", "AMBOS"),
    ("C23", "Archivo y retención documental", 19,
     "¿Existe procedimiento para mantener disponible, controlada y actualizada la documentación y registros del PESV?", "DOCUMENTO"),
    ("C24", "Indicadores y reporte de autogestión PESV", 20,
     "¿Se diligencia el reporte de autogestión anual y se hace seguimiento a los indicadores definidos del PESV?", "AMBOS"),
    ("C25", "Registro y análisis estadístico de siniestros por nivel de pérdida", 21,
     "¿Se registra y analiza estadísticamente la siniestralidad vial por nivel de pérdida?", "AMBOS"),
    ("C26", "Auditorías internas y planes de mejora previos", 22,
     "¿Se han realizado auditorías internas anuales previas y existen planes de mejora derivados de ellas?", "AMBOS"),
    ("C27", "Actualización del PESV", 23,
     "¿El PESV se actualiza periódicamente incorporando acciones preventivas, correctivas y de mejora continua?", "AMBOS"),
    ("C28", "Mecanismos de comunicación y participación", 24,
     "¿Existen mecanismos definidos de comunicación y participación de los colaboradores en el PESV?", "AMBOS"),
]

INSTRUMENTOS = [
    ("Lista de chequeo general PESV (24 pasos)", "LISTA_CHEQUEO", "Instrumento base para verificar documentalmente cada uno de los 24 pasos del PESV."),
    ("Formato de inspección física de vehículos", "INSPECCION_FISICA", "Para la verificación en sitio del estado de los vehículos, SOAT, RTM y elementos de seguridad."),
    ("Formato de entrevista al líder del PESV / CSV", "ENTREVISTA", "Guía de entrevista estructurada para el líder del PESV y miembros del Comité de Seguridad Vial."),
    ("Encuesta de percepción a conductores", "ENCUESTA", "Instrumento para indagar percepción y conocimiento de los conductores sobre el PESV."),
]


class Command(BaseCommand):
    help = "Carga el catálogo oficial de los 24 pasos del PESV (Res. 40595/2022) y los componentes verificables base."

    def handle(self, *args, **options):
        for numero, nombre, fase, nivel in PASOS:
            paso, creado = PasoPESV.objects.update_or_create(
                numero=numero,
                defaults={"nombre": nombre, "fase": fase, "nivel_aplicable": nivel},
            )
            self.stdout.write(f"{'Creado' if creado else 'Actualizado'}: Paso {numero} - {nombre}")

        for orden, (codigo, nombre, paso_num, pregunta, tipo_ev) in enumerate(COMPONENTES, start=1):
            paso = PasoPESV.objects.get(numero=paso_num)
            componente, creado = Componente.objects.update_or_create(
                codigo=codigo,
                defaults={
                    "nombre": nombre,
                    "paso_principal": paso,
                    "pregunta_verificacion": pregunta,
                    "tipo_evidencia_esperada": tipo_ev,
                    "orden": orden,
                    "activo": True,
                },
            )
            self.stdout.write(f"{'Creado' if creado else 'Actualizado'}: {codigo} - {nombre}")

        for nombre, tipo, descripcion in INSTRUMENTOS:
            InstrumentoInspeccion.objects.update_or_create(
                nombre=nombre, defaults={"tipo": tipo, "descripcion": descripcion, "activo": True}
            )

        self.stdout.write(self.style.SUCCESS(
            f"Catálogo cargado: {PasoPESV.objects.count()} pasos, {Componente.objects.count()} componentes, "
            f"{InstrumentoInspeccion.objects.count()} instrumentos."
        ))
