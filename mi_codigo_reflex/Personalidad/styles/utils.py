import reflex as rx

#*Común*#

def lang() -> rx.Component:
    return rx.script("""
                        document.documentElement.lang='es'
                        document.addEventListener('contextmenu', event => event.preventDefault());""")
    
def langg() -> rx.Component:
    return rx.script("""
                        document.documentElement.lang='es'""")


#*Info page*#

titulo = "TEST DE PERSONALIDAD"

descripcion = """La prueba de Personalidad forma parte de la segunda fase de la oposición de Tropa y Marinería. 
También se hace por ordenador. En él debes responder a cada una de las preguntas eligiendo una de las cinco 
opciones que tendrás y que siempre son las mismas:"""

op_1 = "SI"
op_2 = "MUCHAS VECES"
op_3 = "ALGUNAS VECES"
op_4 = "POCAS VECES"
op_5 = "NO"

titulo_2 = "¿Qué evalúan en el Test de Personalidad?"

item_1 = "SINCERIDAD"
item_2 = "DEPRESIÓN"
item_3 = "NEUROTICISMO"
item_4 = "PSICOPATÍA"
item_5 = "PSICOTICISMO"
item_6 = "PARANOIDISMO"
item_7 = "EXTRAVERSIÓN"

desc_1 = """En el test encontrarás algunas preguntas que están encaminadas a comprobar si tiendes a falsear 
tus respuestas porque te parezcan que son socialmente más aceptables en vez responder la opción que realmente 
refleja tu personalidad. Generalmente son preguntas sobre actividades que realizas con frecuencia."""

desc_2 = """También realizan preguntas que pretenden valorar si tienes alterada la capacidad para captar, sentir 
y manifestar los afectos. Quieren comprobar que no estás deprimido. Si lo estás tendrás signos y síntomas como 
pueden ser retraimiento, apatía o ideas delirantes, irritabilidad, ansiedad, dificultad en las relaciones… incluso 
también síntomas físicos."""

desc_3 = """Esta dimensión es fundamental en la personalidad y todos la tenemos en algún grado es la que controla cómo 
respondes a los estímulos externos y cómo reaccionas a los problemas. En el test hay preguntas que valoran tu estabilidad emocional."""

desc_4 = """La psicopatía o personalidad psicopática es un trastorno antisocial de la personalidad que se caracteriza por falta de empatía, 
pobre control de los impulsos y conductas manipulativas. En el test buscarán si tienes tus propios códigos de conducta y te alejas de las 
normas sociales comunes o si sientes las emociones como el resto de las personas, tienes remordimientos, proporcionalidad y empatía."""

desc_5 = """Esta dimensión comprueba tu vulnerabilidad a conductas impulsivas, agresivas o de baja empatía. Comprueban, en función de tus 
respuestas, si tienes una mentalidad desconsiderada, imprudente, hostil, irascible, irracional o impulsiva. Si sientes agrado por sensaciones 
físicas muy fuertes o crueldad inhumana."""

desc_6 = """También comprobarán si tienes un trastorno delirante,  estos trastornos producen un quiebro de la realidad y el enfermo crea una 
nueva dentro de su mente en la que se siente víctima de las acciones de una o varias personas o de una institución, creyendo que actúan en su 
contra y siendo imposible convencerlo de lo contrario por medio de la lógica."""

desc_7 = """Este rasgo podemos definirlo como el deseo y la facilidad que tenemos de contactar con otras, en el test habrá también preguntas 
destinadas a valorar el grado de introversión o extraversión que tienes."""