def find_zodiac_in_topic(topic, burclar):
    # Burçları ve topic'i küçük harfe çevirerek karşılaştırma
    topic_lower = topic.split(" ")

    lower_topic = []
    for t in topic_lower:
        lower_topic.append(t)

    burclar_lower = []  # Burçları küçük harfe çeviren bir listeye ekle

    for b in burclar:
        b = b.lower()
        burclar_lower.append(b)

    for burc in burclar_lower:
        if burc in lower_topic:
            return burc  # Eşleşen burcu döndür
    
    return ""  # Eşleşme yoksa boş döndür