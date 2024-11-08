import re
from nltk.corpus import stopwords
import spacy

stopwords_es = set(stopwords.words('spanish'))
stopwords_en = set(stopwords.words('english'))
nlp = spacy.load('es_core_news_lg')

# Función principal para preprocesar texto
def preprocesar_texto(texto: str) -> list[str]:
  nuevo_texto = pasar_a_minusculas(texto)
  tokens = tokenizar_texto(nuevo_texto)
  tokens = eliminar_ruido(tokens)
  tokens = reducir_palabras_extendidas(tokens)
  tokens = eliminar_stopwords(tokens)
  tokens = limitar_caracteres(tokens)
  tokens = eliminar_espacios(tokens)
  tokens = lematizar_tokens(tokens)
  return tokens

# Paso 1: Convertir el texto a minúsculas
def pasar_a_minusculas(texto: str) -> str:
  texto_str = str(texto)
  return texto_str.lower()

# Paso 2: Tokenizar el texto
# Ejemplo: "Hola, ¿cómo estás?" -> ["Hola,", "¿cómo", "estás?"]
def tokenizar_texto(texto: str) -> list[str]:
  texto_tokenizado = texto.split(' ')
  texto_tokenizado = limpiar_tokens(texto_tokenizado)
  texto_tokenizado_limpio = eliminar_ruido(texto_tokenizado)
  texto_tokenizado_limpio = reducir_palabras_extendidas(texto_tokenizado_limpio)
  return texto_tokenizado_limpio

# Paso 3: Eliminar ruido como URLs, menciones y hashtags
# Ejemplo: ["Hola,"@sebastian, "http://www.google.com", "#InteligenciaArtificial", "¿cómo", "estás?"] -> ["Hola,", "¿cómo", "estás?"]
def eliminar_ruido(tokens: list[str]) -> list[str]:
  if len(tokens) == 0: return []
  # Eliminar URLs
  lista_limpia = []
  for token in tokens:
    if not token.startswith('http'):
      lista_limpia.append(token)
  # Eliminar Hashtags
  lista_limpia = [token for token in lista_limpia if not token.startswith('#')]
  # Eliminar menciones
  lista_limpia = [token for token in lista_limpia if not token.startswith('@')]
  return lista_limpia

# Paso 4: Reducir palabras extendidas
# Ejemplo: ["Holaaaa"] -> ["Hola"]
def reducir_palabras_extendidas(tokens: list[str]) -> list[str]:
  if len(tokens) == 0: return []
  for i in range(len(tokens)):
    tokens[i] = re.sub(r'(.)\1{2,}', r'\1\1', tokens[i])
  return tokens

# Paso 5: Eliminar stopwords
def eliminar_stopwords(tokens: list[str]) -> list[str]:
  if len(tokens) == 0: return []
  tokens_limpio = [token for token in tokens if token not in stopwords_es]
  tokens_limpio = [token for token in tokens_limpio if token not in stopwords_en]
  return tokens_limpio

# Paso 6: Limitar caracteres solo a letras
def limitar_caracteres(tokens: list[str]) -> list[str]:
  if len(tokens) == 0: return []
  tokens_limpio = eliminar_acentos(tokens)
  tokens_limpio = [re.sub(r'[^a-zA-Z]', '', token) for token in tokens_limpio]
  tokens_limpio = limpiar_tokens(tokens_limpio)
  return tokens_limpio

# Paso 7: Eliminar espacios en blanco adicionales
def eliminar_espacios(tokens: list[str]) -> list[str]:
  if len(tokens) == 0: return []
  tokens_limpio = limpiar_tokens(tokens)
  tokens_limpio = [token.strip() for token in tokens]
  return tokens_limpio

# Paso 8: Lematizar tokens
def lematizar_tokens(tokens: list[str]) -> list[str]:
  if len(tokens) == 0: return []
  tokens_lematizados = []
  for token in tokens:
      doc = nlp(token)
      # Obtener la primera palabra lematizada
      lemma = doc[0].lemma_.split()[0]
      tokens_lematizados.append(lemma)
  return tokens_lematizados

# Helper 1: Limpiar tokens
# Ejemplo: ["Hola,", "", "¿cómo", "estás?"] -> ["Hola,", "¿cómo", "estás?"]
def limpiar_tokens(tokens: list[str]) -> list[str]:
  if len(tokens) == 0: return []
  tokens_limpio = [token for token in tokens if token != '']
  return tokens_limpio

# Helper 2: Eliminar acentos
# Ejemplo: ["Hóla", "¿cómo", "estás?"] -> ["Hola", "¿como", "estas?"]
def eliminar_acentos(tokens: list[str]) -> list[str]:
  if len(tokens) == 0: return []
  tokens_copy = tokens.copy()
  for i in range(len(tokens_copy)):
    tokens_copy[i] = tokens_copy[i].replace('á', 'a').replace('Á', 'A').replace('ä', 'a').replace('Ä', 'A').replace('à', 'a').replace('À', 'A').replace('â', 'a').replace('Â', 'A')
    tokens_copy[i] = tokens_copy[i].replace('é', 'e').replace('É', 'E').replace('ë', 'e').replace('Ë', 'E').replace('è', 'e').replace('È', 'E').replace('ê', 'e').replace('Ê', 'E')
    tokens_copy[i] = tokens_copy[i].replace('í', 'i').replace('Í', 'I').replace('ï', 'i').replace('Ï', 'I').replace('ì', 'i').replace('Ì', 'I').replace('î', 'i').replace('Î', 'I')
    tokens_copy[i] = tokens_copy[i].replace('ó', 'o').replace('Ó', 'O').replace('ö', 'o').replace('Ö', 'O').replace('ò', 'o').replace('Ò', 'O').replace('ô', 'o').replace('Ô', 'O')
    tokens_copy[i] = tokens_copy[i].replace('ú', 'u').replace('Ú', 'U').replace('ü', 'u').replace('Ü', 'U').replace('ù', 'u').replace('Ù', 'U').replace('û', 'u').replace('Û', 'U')
    tokens_copy[i] = tokens_copy[i].replace('ñ', 'n')
  return tokens_copy

# Helper 3: Eliminar acentos pero solo para una palabra
def eliminar_acentos_palabra(palabra: str) -> str:
  palabra_limpia = palabra.replace('á', 'a').replace('Á', 'A').replace('ä', 'a').replace('Ä', 'A').replace('à', 'a').replace('À', 'A').replace('â', 'a').replace('Â', 'A')
  palabra_limpia = palabra_limpia.replace('é', 'e').replace('É', 'E').replace('ë', 'e').replace('Ë', 'E').replace('è', 'e').replace('È', 'E').replace('ê', 'e').replace('Ê', 'E')
  palabra_limpia = palabra_limpia.replace('í', 'i').replace('Í', 'I').replace('ï', 'i').replace('Ï', 'I').replace('ì', 'i').replace('Ì', 'I').replace('î', 'i').replace('Î', 'I')
  palabra_limpia = palabra_limpia.replace('ó', 'o').replace('Ó', 'O').replace('ö', 'o').replace('Ö', 'O').replace('ò', 'o').replace('Ò', 'O').replace('ô', 'o').replace('Ô', 'O')
  palabra_limpia = palabra_limpia.replace('ú', 'u').replace('Ú', 'U').replace('ü', 'u').replace('Ü', 'U').replace('ù', 'u').replace('Ù', 'U').replace('û', 'u').replace('Û', 'U')
  palabra_limpia = palabra_limpia.replace('ñ', 'n')
  return palabra_limpia