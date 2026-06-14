import time

def scrape_hepsiburada(page, url):
    print(f"Hepsiburada süreci başladı: {url}")
    
    # giriş kısmı
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(2000)
        
        review_link = page.locator('[data-test-id="has-review"] a').first
        if review_link.is_visible():
            review_link.click()
            page.wait_for_timeout(3000)
        elif "/yorumlari" not in url:
            hedef_url = url.split("-p-")[0] + "-yorumlari"
            page.goto(hedef_url, wait_until="networkidle")
    except Exception as e:
        print(f"Hepsiburada giriş hatası: {e}")

    # sıralama
    try:
        page.click('[class*="hermes-Sort-module-VANnZ3"]', timeout=5000)
        page.wait_for_timeout(1000)
        page.locator('text="En yeni değerlendirme"').first.click(force=True)
        page.wait_for_timeout(3000)
    except:
        pass

    all_data = []
    seen_texts = set()
    current_page = 1 
    
    # sayfalardan veri toplama
    while True:
        print(f"Hepsiburada: Sayfa {current_page} taranıyor... (Mevcut: {len(all_data)})")
        
        # Sayfayı kaydır ve yorumların yüklenmesini bekle
        for _ in range(6):
            page.mouse.wheel(0, 1000)
            page.wait_for_timeout(600)

        # kartların belirlenmesi
        try:
            page.wait_for_selector('[class*="ReviewCard-module-dY_oaYMIo"]', timeout=5000)
        except:
            print("Hepsiburada: Bu sayfada yorum kartı bulunamadı, bitiriliyor.")
            break

        cards = page.locator('[class*="ReviewCard-module-dY_oaYMIo"]').all()
        
        for card in cards:
            try:
                metin_locator = card.locator('[class*="ReviewCard-module-KaU17Bb"]').first
                if metin_locator.count() > 0:
                    metin = metin_locator.inner_text().strip()
                    if len(metin) >= 15 and metin not in seen_texts:
                        try:
                            satici = card.locator('span[role="button"]').first.inner_text().strip()
                        except:
                            satici = "Hepsiburada Satıcısı"
                        all_data.append((satici, metin))
                        seen_texts.add(metin)
            except:
                continue

        target_page = current_page + 1
        # bir sonraki sayfa var mı
        next_page_btn = page.locator(f'div[class*="paginationBarHolder"] span:text-is("{target_page}")').first
        
        # sayfa yoksa dur
        if not next_page_btn.is_visible(timeout=4000):
            print(f"Hepsiburada: {target_page}. sayfa rakamı bulunamadı. Tarama son sayfada (Sayfa {current_page}) bitti.")
            break
        
        # rakam varsa tıkla
        print(f"Hepsiburada: {target_page}. sayfaya geçiliyor...")
        next_page_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        next_page_btn.click(force=True)
        
        current_page = target_page
        page.wait_for_timeout(4000) # sayfanın yüklenmesi için zaman
        page.keyboard.press("Home")

    # değerlendirme çıktı
    print(f"\n--- TARAMA TAMAMLANDI ---")
    print(f"Toplam Çekilen Yorum: {len(all_data)}")
    return all_data