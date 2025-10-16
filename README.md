# Analytics & Data Engineering Portfolio

<div align="center">

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)

**[English](#english)** | **[Русский](#russian)** | **[Quick Start for Recruiters](QUICK_START.md)**

</div>

---

<a name="english"></a>
## English Version

### About

Welcome to my professional portfolio — a curated collection of projects demonstrating expertise in **data engineering**, **ETL development**, **web scraping**, and **computer vision**. 

All work presented here:
- Represents real-world professional experience with anonymized data
- Showcases production-ready code and solutions
- Fully complies with NDA and confidentiality requirements
- Demonstrates best practices in software engineering

### Core Competencies

**Programming & Tools:**  
`Python` · `SQL` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Jupyter Notebook`

**Data Engineering & Analytics:**  
`ETL Pipelines` · `OpenSearch/Elasticsearch` · `Multithreading` · `Data Optimization` · `Big Data Processing` · `Statistical Analysis` · `A/B Testing` · `SciPy`

**Web Development & Scraping:**  
`FastAPI` · `Playwright` · `Asyncio` · `Streamlit` · `RESTful APIs`

**Computer Vision:**  
`OpenCV` · `YOLO (Ultralytics)` · `Shapely` · `Real-time Detection`

**DevOps & Infrastructure:**  
`Docker` · `Git` · `Linux` · `Telegram Bots` · `Containerization`

---

### Featured Projects

<table>
<thead>
  <tr>
    <th width="30%">Project</th>
    <th width="50%">Description</th>
    <th width="20%">Links</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><strong>Multithreaded Data Downloader</strong><br><em>(Professional — Gear Games)</em></td>
    <td>
      High-performance ETL tool developed for Gear Games analytics department. Extracts large datasets from OpenSearch/Elasticsearch with intelligent query sharding, parallel processing, memory optimization, and progress monitoring. Actively used by analytics team and automated scripts.
      <br><br>
      <strong>Key achievements:</strong>
      <ul>
        <li>Reduced extraction time by <strong>30x</strong> (68 days → 2.27 days)</li>
        <li><strong>9.1+ billion rows</strong> extracted by analytics team in 1 month</li>
        <li>Cut memory usage by <strong>55%</strong> through optimization</li>
      </ul>
      <strong>Tech:</strong> Python, ThreadPoolExecutor, Pandas, Memory Profiling, Caching
    </td>
    <td>
      <a href="/common/concurrent_data_downloader.py">Code</a>
      <br>
      <a href="/eng/1.%20Multithreaded%20Data%20Downloading.md">Details</a>
    </td>
  </tr>
  <tr>
    <td><strong>Vulkan FPS Impact Analysis</strong><br><em>(Professional Analytical Research — Gear Games)</em></td>
    <td>
      Production-grade statistical analysis framework for evaluating Vulkan API implementation impact on player FPS performance across mobile devices. Developed for Gear Games to guide platform-specific graphics API deployment decisions, ensuring optimal player experience. <em>Repository includes synthetic data example maintaining analytical methodology.</em>
      <br><br>
      <strong>Key achievements:</strong>
      <ul>
        <li>Analyzed <strong>1,298 players</strong> with paired before/after testing methodology</li>
        <li>Identified <strong>31 device models</strong> with statistically stable FPS improvement (>70% improvement rate)</li>
        <li>Identified <strong>37 device models</strong> with FPS degradation requiring Vulkan rollback (<30% improvement rate)</li>
        <li>Classified <strong>10 GPU families</strong> for Vulkan enablement and <strong>12 for exclusion</strong></li>
        <li>Applied <strong>rigorous statistical methodology</strong> with paired t-tests and significance testing to validate findings</li>
        <li>Delivered <strong>comprehensive analytical visualizations</strong>: distribution plots, box plots, scatter matrices, and segment-specific performance charts</li>
      </ul>
      <strong>Tech:</strong> Python, Pandas, NumPy, SciPy (t-tests), Matplotlib, Seaborn, Statistical Analysis
    </td>
    <td>
      <a href="/common/vulkan_fps_analysis/">Code</a>
      <br>
      <a href="/eng/2.%20Vulkan%20FPS%20Impact%20Analysis.md">Details</a>
    </td>
  </tr>
  <tr>
    <td><strong>GG-Bet Tournament Platform</strong><br><em>(Professional — Gear Games)</em></td>
    <td>
      Enterprise-grade internal betting platform developed for Gear Games annual company tournament. Features real-time betting engine, comprehensive event management, dynamic odds calculation, role-based access control, and analytics dashboard. Used by employees for entertainment during competitive gaming events.
      <br><br>
      <strong>Tournament achievements:</strong>
      <ul>
        <li><strong>68 participants</strong> with <strong>99% engagement rate</strong> (67 active users)</li>
        <li><strong>1,100 bets</strong> processed in 48 hours across 49 tournament events</li>
        <li><strong>1,865 financial transactions</strong> with zero integrity errors (ACID compliance)</li>
        <li><strong>11.6M+ credits</strong> in total betting volume handled</li>
        <li>Average <strong>16 bets per user</strong> demonstrating strong platform adoption</li>
      </ul>
      <strong>Tech:</strong> Python, FastAPI, SQLModel, SQLite, Bcrypt, HTML/CSS, Jinja2
    </td>
    <td>
      <a href="https://github.com/ahruslan17/gg-bet">Repository</a>
    </td>
  </tr>
  <tr>
    <td><strong>BetBoom Odds Parser</strong><br><em>(Pet Project)</em></td>
    <td>
      Automated scraper for real-time basketball betting odds from betboom.ru. Features dynamic odds tracking, scheduled data collection, and Docker containerization.
      <br><br>
      <strong>Tech:</strong> Python, Playwright, Asyncio, Docker, CSV
    </td>
    <td>
      <a href="https://github.com/ahruslan17/betboom_totals_parser">Repository</a>
    </td>
  </tr>
  <tr>
    <td><strong>Russian Wordle Assistant</strong><br><em>(Pet Project)</em></td>
    <td>
      Interactive Streamlit application helping users solve the Russian Wordle game by tracking guesses, applying constraints, and filtering possible solutions.
      <br><br>
      <strong>Tech:</strong> Python, Streamlit, NLP, Algorithms
    </td>
    <td>
      <a href="https://github.com/ahruslan17/russian_wordle_assistant">Repository</a>
    </td>
  </tr>
  <tr>
    <td><strong>CV Parking Monitoring</strong><br><em>(Pet Project)</em></td>
    <td>
      End-to-end computer vision system for parking lot analytics. Features interactive zone labeling, YOLO-based vehicle detection, real-time availability calculation, and Telegram bot integration for on-demand monitoring.
      <br><br>
      <strong>Tech:</strong> OpenCV, YOLO, Shapely, Python-telegram-bot, JSON
    </td>
    <td>
      <a href="https://github.com/ahruslan17/CVPM">Repository</a>
    </td>
  </tr>
</tbody>
</table>

---

### Contact

Interested in collaboration or have questions? Feel free to reach out:

**Telegram:** [@ahruslan01](https://t.me/ahruslan01)  
**Email:** [ahruslan17@gmail.com](mailto:ahruslan17@gmail.com)

---

<a name="russian"></a>
## Русская версия

### О портфолио

Добро пожаловать в мое профессиональное портфолио — тщательно подобранная коллекция проектов, демонстрирующих экспертизу в **инженерии данных**, **разработке ETL**, **веб-скрейпинге** и **компьютерном зрении**.

Все представленные работы:
- Представляют реальный профессиональный опыт с обезличенными данными
- Демонстрируют production-готовый код и решения
- Полностью соответствуют требованиям NDA и конфиденциальности
- Демонстрируют лучшие практики программной инженерии

### Ключевые компетенции

**Программирование и инструменты:**  
`Python` · `SQL` · `Pandas` · `NumPy` · `Matplotlib` · `Seaborn` · `Jupyter Notebook`

**Инженерия данных и аналитика:**  
`ETL Пайплайны` · `OpenSearch/Elasticsearch` · `Многопоточность` · `Оптимизация данных` · `Big Data` · `Статистический анализ` · `A/B тестирование` · `SciPy`

**Веб-разработка и парсинг:**  
`FastAPI` · `Playwright` · `Asyncio` · `Streamlit` · `RESTful APIs`

**Компьютерное зрение:**  
`OpenCV` · `YOLO (Ultralytics)` · `Shapely` · `Детекция в реальном времени`

**DevOps и инфраструктура:**  
`Docker` · `Git` · `Linux` · `Telegram боты` · `Контейнеризация`

---

### Избранные проекты

<table>
<thead>
  <tr>
    <th width="30%">Проект</th>
    <th width="50%">Описание</th>
    <th width="20%">Ссылки</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td><strong>Многопоточная выгрузка данных</strong><br><em>(Профессиональный — Gear Games)</em></td>
    <td>
      Высокопроизводительный ETL-инструмент, разработанный для отдела аналитики Gear Games. Извлекает большие объёмы данных из OpenSearch/Elasticsearch с интеллектуальным шардированием запросов, параллельной обработкой, оптимизацией памяти и мониторингом прогресса. Активно используется командой аналитиков и автоматизированными скриптами.
      <br><br>
      <strong>Ключевые достижения:</strong>
      <ul>
        <li>Сокращение времени выгрузки в <strong>30 раз</strong> (68 дней → 2,27 дня)</li>
        <li><strong>9,1+ млрд строк</strong> выгружено командой аналитики за 1 месяц</li>
        <li>Снижение потребления памяти на <strong>55%</strong> через оптимизацию</li>
      </ul>
      <strong>Технологии:</strong> Python, ThreadPoolExecutor, Pandas, Memory Profiling, Кэширование
    </td>
    <td>
      <a href="/common/concurrent_data_downloader.py">Код</a>
      <br>
      <a href="/ru/1.%20Многопоточная%20выгрузка%20данных.md">Детали</a>
    </td>
  </tr>
  <tr>
    <td><strong>Анализ влияния Vulkan на FPS</strong><br><em>(Профессиональное аналитическое исследование — Gear Games)</em></td>
    <td>
      Production-ready фреймворк для статистического анализа влияния внедрения Vulkan API на производительность FPS игроков на мобильных устройствах. Разработан для Gear Games для принятия решений о платформо-специфичном развёртывании графического API, обеспечивая оптимальный игровой опыт. <em>В репозитории представлен пример на синтетических данных с сохранением методологии анализа.</em>
      <br><br>
      <strong>Ключевые достижения:</strong>
      <ul>
        <li>Проанализировано <strong>1 298 игроков</strong> с методологией парного сравнения до/после</li>
        <li>Выявлено <strong>31 модель устройств</strong> со стабильным улучшением FPS (>70% improvement rate)</li>
        <li>Выявлено <strong>37 моделей устройств</strong> с деградацией FPS, требующих отката Vulkan (<30% improvement rate)</li>
        <li>Классифицировано <strong>10 семейств GPU</strong> для включения Vulkan и <strong>12 для исключения</strong></li>
        <li>Применена <strong>строгая статистическая методология</strong> с парными t-тестами и проверкой значимости для валидации результатов</li>
        <li>Разработаны <strong>комплексные аналитические визуализации</strong>: графики распределений, box plots, scatter-матрицы и сегментированные диаграммы производительности</li>
      </ul>
      <strong>Технологии:</strong> Python, Pandas, NumPy, SciPy (t-тесты), Matplotlib, Seaborn, Статистический анализ
    </td>
    <td>
      <a href="/common/vulkan_fps_analysis/">Код</a>
      <br>
      <a href="/ru/2.%20Анализ%20влияния%20Vulkan%20на%20FPS.md">Детали</a>
    </td>
  </tr>
  <tr>
    <td><strong>GG-Bet Tournament Platform</strong><br><em>(Профессиональный — Gear Games)</em></td>
    <td>
      Корпоративная платформа для внутреннего беттинга, разработанная для ежегодного турнира компании Gear Games. Включает движок ставок в реальном времени, комплексную систему управления событиями, динамический расчёт коэффициентов, ролевое управление доступом и аналитическую панель. Используется сотрудниками для развлечения во время игровых соревнований.
      <br><br>
      <strong>Достижения турнира:</strong>
      <ul>
        <li><strong>68 участников</strong> с <strong>99% вовлечённостью</strong> (67 активных пользователей)</li>
        <li><strong>1 100 ставок</strong> обработано за 48 часов в рамках 49 турнирных событий</li>
        <li><strong>1 865 финансовых транзакций</strong> без ошибок целостности (ACID-совместимость)</li>
        <li><strong>11,6 млн+ кредитов</strong> обработано в общем объёме ставок</li>
        <li>Среднее <strong>16 ставок на пользователя</strong> — высокий уровень принятия платформы</li>
      </ul>
      <strong>Технологии:</strong> Python, FastAPI, SQLModel, SQLite, Bcrypt, HTML/CSS, Jinja2
    </td>
    <td>
      <a href="https://github.com/ahruslan17/gg-bet">Репозиторий</a>
    </td>
  </tr>
  <tr>
    <td><strong>Парсер коэффициентов BetBoom</strong><br><em>(Pet-проект)</em></td>
    <td>
      Автоматизированный сбор коэффициентов ставок на баскетбол в реальном времени с сайта betboom.ru. Динамическое отслеживание коэффициентов, запланированный сбор данных, Docker-контейнеризация.
      <br><br>
      <strong>Технологии:</strong> Python, Playwright, Asyncio, Docker, CSV
    </td>
    <td>
      <a href="https://github.com/ahruslan17/betboom_totals_parser">Репозиторий</a>
    </td>
  </tr>
  <tr>
    <td><strong>Ассистент для игры 5 букв</strong><br><em>(Pet-проект)</em></td>
    <td>
      Интерактивное Streamlit-приложение для решения русской версии игры Wordle путём отслеживания попыток, применения ограничений и фильтрации возможных решений.
      <br><br>
      <strong>Технологии:</strong> Python, Streamlit, NLP, Алгоритмы
    </td>
    <td>
      <a href="https://github.com/ahruslan17/russian_wordle_assistant">Репозиторий</a>
    </td>
  </tr>
  <tr>
    <td><strong>Мониторинг парковки (CV)</strong><br><em>(Pet-проект)</em></td>
    <td>
      Полнофункциональная система компьютерного зрения для аналитики парковки. Интерактивная разметка зон, детекция автомобилей на основе YOLO, расчёт доступности в реальном времени и интеграция с Telegram-ботом для мониторинга по запросу.
      <br><br>
      <strong>Технологии:</strong> OpenCV, YOLO, Shapely, Python-telegram-bot, JSON
    </td>
    <td>
      <a href="https://github.com/ahruslan17/CVPM">Репозиторий</a>
    </td>
  </tr>
</tbody>
</table>

---

### Контакты

Заинтересованы в сотрудничестве или есть вопросы? Свяжитесь со мной:

**Telegram:** [@ahruslan01](https://t.me/ahruslan01)  
**Email:** [ahruslan17@gmail.com](mailto:ahruslan17@gmail.com)

---

<div align="center">

**Thank you for visiting my portfolio! | Спасибо за внимание к моему портфолио!**

*This portfolio is regularly updated with new projects and improvements.*  
*Портфолио регулярно обновляется новыми проектами и улучшениями.*

</div>
