import time

def scrape_n11(page, url):
    print(f"n11 süreci başladı: {url}")
    
    # tarama süresi 90 saniye
    page.goto(url, wait_until="networkidle", timeout=90000)
    
    try:
        print("n11: Tüm yorumlar sayfasına geçiliyor...")
        page.click(".product-reviews__link", timeout=7000)
        page.wait_for_timeout(3000)
    except Exception as e:
        print("n11: Yorumlar sekmesi zaten açık olabilir veya buton bulunamadı.")

    # kaydırmaya ve aramaya başlama
    last_count = 0
    no_change_count = 0
    max_scroll = 50  # kaydırma sayısı
    
    print("n11: Derin ve dinamik tarama başlatıldı...")

    for i in range(max_scroll):
        page.keyboard.press("PageDown")
        
        # yükleme beklemesi
        page.wait_for_timeout(1200) 
        
        # kaç yorum kutusu var kontrol
        current_count = page.locator(".review-card").count()
        
        if current_count > last_count:
            # yeni yorumlar geldikçe devam
            print(f"Yeni veriler yüklendi... Mevcut sayı: {current_count}")
            last_count = current_count
            no_change_count = 0 
        else:
            # veri gelmezse bekleme 2.5 saniye
            print("Yeni veri bekleniyor, bağlantı yavaş olabilir...")
            page.wait_for_timeout(2500)
            no_change_count += 1
            
            # Daha Fazla Göster butonu varsa
            try:
                more_button = page.locator("text='Daha Fazla Göster'")
                if more_button.is_visible():
                    more_button.click()
                    print("n11: 'Daha Fazla Göster' butonuna tıklandı.")
                    page.wait_for_timeout(2000)
                    no_change_count = 0 
            except:
                pass

        # yeni veri gelmezse döngüyü kır (4)
        if no_change_count >= 4:
            print("Sayfa sonuna ulaşıldı veya veri akışı durdu.")
            break

    # veri toplama
    cards = page.locator(".review-card").all()
    data = []
    
    try:
        ana_satici = page.locator(".shop-name, .seller-name").first.inner_text()
    except:
        ana_satici = "n11 Satıcısı"

    print(f"Analiz edilecek toplam yorum kutusu: {len(cards)}")

    for card in cards:
        try:
            metin = card.locator(".card-detail__contents").inner_text().strip()
            try:
                satici = card.locator(".card-detail__seller_nickname span").first.inner_text().strip()
            except:
                satici = ana_satici
                
            if len(metin) > 5:
                data.append((satici, metin))
        except:
            continue
            
    print(f"n11: Toplam {len(data)} yorum başarıyla toplandı.")
    return data