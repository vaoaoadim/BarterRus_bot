from database import get_ads

def format_ad(ad):
    _, direction, category, title, description, contact = ad
    direction_text = "📢 Реклама за товар/услугу" if direction == "ad_for_product" else "🎁 Товар/услуга за рекламу"
    return (
        f"{direction_text}\n"
        f"📂 Категория: {category}\n"
        f"📌 {title}\n"
        f"📝 {description}\n"
        f"📞 Контакт: {contact}"
    )

def search_ads(direction=None, keyword=None, category=None, exclude_contact=None):
    ads = get_ads(direction, keyword, category)
    if exclude_contact:
        ads = [ad for ad in ads if ad[5] != exclude_contact]
    return ads
