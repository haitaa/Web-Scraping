import re 

def metni_duzenle(text):
  """Noktalama işaretlerini kaldırarak her kelimeyi listeye ayır"""
  cleaned_text = re.sub(r'[^\w\s]', '', text)
  words = cleaned_text.split()

  unique_words = list(set(words))

  return unique_words

