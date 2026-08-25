/**
 * Portfolio of niches under portrait: founders / entrepreneurs.
 * Status: backlog | testing | keep | paused | killed
 * Only niches with graph data can be shown on the map.
 */
window.TOOLMAP_NICHES = {
  portrait: {
    id: "founders-entrepreneurs",
    label: "Фаундеры и предприниматели",
    blurb: "Соло и микрокоманды, которые сами собирают digital-стек под продукт или услуги.",
  },
  activeSlug: "solo-digital-services",
  items: [
    {
      slug: "solo-digital-services",
      label: "Соло digital-услуги / инфобизнес",
      status: "testing",
      audience: "Фаундер услуг или простого digital-продукта (гайд, мини-курс, консультации).",
      nodes: [
        { id: "notion", label: "Notion", x: 180, y: 120, blurb: "Операционка: клиенты, оффер, задачи, база знаний." },
        { id: "telegram", label: "Telegram", x: 420, y: 80, blurb: "Канал, бот, поддержка, прогрев аудитории." },
        { id: "tilda", label: "Tilda", x: 660, y: 120, blurb: "Лендинг оффера и сбор заявок." },
        { id: "sheets", label: "Google Sheets", x: 180, y: 280, blurb: "Учёт лидов, денег, простой CRM-слой." },
        { id: "pay", label: "ЮKassa / Stripe", x: 420, y: 260, blurb: "Приём оплаты за услугу или гайд." },
        { id: "canva", label: "Canva", x: 660, y: 280, blurb: "Креативы для канала и лендинга." },
        { id: "cal", label: "Calendly / Cal.com", x: 300, y: 420, blurb: "Запись на созвон / консультацию." },
        { id: "ai", label: "ChatGPT", x: 560, y: 420, blurb: "Черновики текстов, разбор интервью, идеи оффера." },
      ],
      edges: [
        { id: "e1", from: "notion", to: "telegram", title: "Контент из Notion → канал", example: "План постов и сниппеты живут в Notion; публикация и прогрев — в Telegram." },
        { id: "e2", from: "telegram", to: "tilda", title: "Трафик канала → лендинг", example: "В посте — ссылка на Tilda с UTM; заявка уходит дальше в учёт." },
        { id: "e3", from: "tilda", to: "sheets", title: "Заявка → таблица", example: "Форма на Tilda пишет строку в Google Sheets (имя, контакт, источник)." },
        { id: "e4", from: "tilda", to: "pay", title: "Оплата с лендинга", example: "Кнопка «Купить» ведёт на ЮKassa/Stripe; после оплаты — доступ к материалу." },
        { id: "e5", from: "sheets", to: "cal", title: "Квалификация → слот", example: "Горячий лид из Sheets получает ссылку Calendly на разбор." },
        { id: "e6", from: "canva", to: "telegram", title: "Креатив → пост", example: "Обложки и карусели из Canva публикуются в канале по календарю." },
        { id: "e7", from: "ai", to: "notion", title: "Черновик → структура", example: "Разбор Mom Test в ChatGPT → карточка клиента и гипотеза в Notion." },
        { id: "e8", from: "ai", to: "tilda", title: "Текст оффера → лендинг", example: "Первый экран и FAQ генерируются как черновик, правятся руками на Tilda." },
      ],
    },
    {
      slug: "micro-saas-founders",
      label: "Микро-SaaS / indie founders",
      status: "backlog",
      audience: "Фаундер микро-SaaS: билдит, меряет, продаёт сам.",
      nodes: null,
      edges: null,
    },
  ],
};
