from src.helpers.text import preprocesar_texto

texto = 'Hola, ¿cómo estás? hoy me siento regulinchis y tengo ganas de ser un lider en la vida totalmente normal no? ✌️ #InteligenciaArtificial'
text2 = 'Comunicación en las daily, creatividad mucha porque debemos dar solución. #InteligenciaArtificial'
result = preprocesar_texto(texto)
result2 = preprocesar_texto(text2)
print(result)
print(result2)