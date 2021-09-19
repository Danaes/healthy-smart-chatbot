form = [
    "Hola {username}. Estoy aquí para ayudarte \U0001F603",
    "Primero necesito hacer unas series de preguntas para conocerte mejor y así ofrecete un servicio "
    "excelente \U0001F60A",
    "¿Cuánto mides (en centímetros)?",
    "¿Cuánto pesas (en kilogramos)?",
    "¿Tienes algún tipo de enfermedad? Si es que sí, dime cual/es",
    "¿Tienes algún tipo de alergia alimentaria? Si es que sí, dime a que",
    "Gracias {username} por dedicarme parte de tu tiempo, voy a analizar los datos que me has facilitado para poder "
    "ofrecerte una dieta acorde al objetivo recomendado. Para obtener la dieta tienes que pulsar en /dieta y te la "
    "enviaré en un momento"
]

objectives = [
    "Tu índice de masa corporal está por debajo de los valores recomendados, te voy a proporcionar una dieta alta en "
    "calorias para alcanzar un peso adecuado a tu altura de {height}cm",
    "Tu índice de masa corporal se encuentra dentro de los valores normales para la altura de {height}cm, mi "
    "recomendación en llevar una dieta equilibrada complementándolo con el deporte que más te guste",
    "Tu índice de masa corporal está por encima de los valores recomendados, te voy a proporcionar una dieta un poco "
    "baja en calorias para alcanzar un peso adecuado a tu altura de {height}cm",
    "Tu índice de masa corporal está muy por encima de los valores recomendados, te voy a proporcionar una dieta baja "
    "en calorias para reducir la obesidad y así alcanzar un peso adecuado a tu altura de {height}cm",
]

columns = ["height", "weight", "disease", "allergy"]

final_response = 'Los resultados obtenidos son los siguientes:\n\n{objective} {allergies} {diseases}'

help = "No te preocupes si no sabes que hacer, estoy aquí para ayudarte. Si pulsas el comando /comenzar iniciaré un " \
       "proceso de preguntas con las cuales te podré conocerte mejor y así, podré ofrecerte una dieta ajustada a tus " \
       "necesidades. Una vez acabado el cuestionario, con el comando /dieta podrás descargar la dieta semanal que " \
       "deberás seguir para alcancer el bienestar "


def format_allergies_and_diseases(types):
    allergies = '\n\nHe detectado que tienes las siguientes alergias: {allergy}.'
    diseases = '\n\nHe detectado que tienes las siguientes enfermedades: {disease}.'

    if types['allergy'] is not None and len(types['allergy']) == 1:
        allergies = allergies.replace('las siguientes alergias', 'la siguiente alergia')

    if types['disease'] is not None and len(types['disease']) == 1:
        diseases = diseases.replace('las siguientes enfermedades', 'la siguiente enfermedad')

    return allergies, diseases
