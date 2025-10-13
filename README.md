# Analytics & Data Engineering Portfolio

<div align="center">

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
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
`Python` · `SQL` · `Pandas` · `NumPy` · `Matplotlib` · `Jupyter Notebook`

**Data Engineering:**  
`ETL Pipelines` · `OpenSearch/Elasticsearch` · `Multithreading` · `Data Optimization` · `Big Data Processing`

**Web Development & Scraping:**  
`Playwright` · `Asyncio` · `Streamlit` · `RESTful APIs`

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
    <td><strong>Multithreaded Data Downloader</strong></td>
    <td>
      High-performance ETL tool for extracting large datasets from OpenSearch/Elasticsearch with intelligent query sharding, parallel processing, memory optimization, and progress monitoring.
      <br><br>
      <strong>Key achievements:</strong>
      <ul>
        <li>Reduced extraction time by <strong>30x</strong> (68 days → 2.27 days)</li>
        <li>Processed <strong>9.1+ billion</strong> rows for analytics</li>
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
    <td><strong>BetBoom Odds Parser</strong></td>
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
    <td><strong>Russian Wordle Assistant</strong></td>
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
    <td><strong>CV Parking Monitoring</strong></td>
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

### Project Highlights

**Multithreaded Data Downloader** stands out as the flagship project, demonstrating:

- **Scalability**: Handled 9.1 billion rows of production data
- **Performance**: 30x speed improvement through intelligent parallelization
- **Efficiency**: 55% memory reduction via type optimization and chunked processing
- **Production-Ready**: Integrated logging, error handling, container support

<details>
<summary><strong>Performance Metrics</strong></summary>

```
Sequential Processing:   1,639 hours (68 days)
Parallel Processing:     54 hours (2.27 days)
Speedup:                 30x improvement

Memory Before Optimization:  9,003 MB peak / 5,779 MB DataFrame
Memory After Optimization:   4,028 MB peak / 3,975 MB DataFrame
Reduction:                   55% memory savings
```
</details>

---

### Contact

Interested in collaboration or have questions? Feel free to reach out via private message to discuss opportunities.

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
`Python` · `SQL` · `Pandas` · `NumPy` · `Matplotlib` · `Jupyter Notebook`

**Инженерия данных:**  
`ETL Пайплайны` · `OpenSearch/Elasticsearch` · `Многопоточность` · `Оптимизация данных` · `Big Data`

**Веб-разработка и парсинг:**  
`Playwright` · `Asyncio` · `Streamlit` · `RESTful APIs`

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
    <td><strong>Многопоточная выгрузка данных</strong></td>
    <td>
      Высокопроизводительный ETL-инструмент для извлечения больших объёмов данных из OpenSearch/Elasticsearch с интеллектуальным шардированием запросов, параллельной обработкой, оптимизацией памяти и мониторингом прогресса.
      <br><br>
      <strong>Ключевые достижения:</strong>
      <ul>
        <li>Сокращение времени выгрузки в <strong>30 раз</strong> (68 дней → 2,27 дня)</li>
        <li>Обработано более <strong>9,1 млрд</strong> строк для аналитики</li>
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
    <td><strong>Парсер коэффициентов BetBoom</strong></td>
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
    <td><strong>Ассистент для игры 5 букв</strong></td>
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
    <td><strong>Мониторинг парковки (CV)</strong></td>
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

### Основные достижения

Проект **Многопоточная выгрузка данных** является флагманским, демонстрируя:

- **Масштабируемость**: Обработка 9,1 млрд строк продакшн-данных
- **Производительность**: Ускорение в 30 раз за счёт интеллектуальной параллелизации
- **Эффективность**: Снижение потребления памяти на 55% через оптимизацию типов и чанковую обработку
- **Production-Ready**: Интегрированное логирование, обработка ошибок, поддержка контейнеров

<details>
<summary><strong>Метрики производительности</strong></summary>

```
Последовательная обработка:  1 639 часов (68 дней)
Параллельная обработка:      54 часа (2,27 дня)
Ускорение:                   в 30 раз

Память до оптимизации:       9 003 МБ пик / 5 779 МБ DataFrame
Память после оптимизации:    4 028 МБ пик / 3 975 МБ DataFrame
Снижение:                    экономия памяти 55%
```
</details>

---

### Контакты

Заинтересованы в сотрудничестве или есть вопросы? Свяжитесь со мной через личные сообщения для обсуждения возможностей.

---

<div align="center">

**Thank you for visiting my portfolio! | Спасибо за внимание к моему портфолио!**

*This portfolio is regularly updated with new projects and improvements.*  
*Портфолио регулярно обновляется новыми проектами и улучшениями.*

</div>
