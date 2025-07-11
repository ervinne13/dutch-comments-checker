# Postman Test Runner Maintenance Instructions

You are an agent that maintains a CSV file of test cases for the Dutch Comments Checker API.

## Instructions

- Read `app/main.py` for all endpoints except `/openapi.json`.
- For `/api/v1/check_comment`, generate a CSV file named `postman_dcc_collection_examples.csv` with the following columns:
  - `subject`
  - `context`
  - `comment`
  - `ham`
  - `spam`
  - `toxic`
- Each row should be a realistic Dutch example, covering:
  - Deliberate spam comments
  - Deliberate toxic comments
  - Grey area comments
  - Normal comments
  - Sarcastic, heated, or problematic comments (not actual spam or toxic)
- Use a variety of topics (e.g., football, news, betting, etc.).
- For each example, provide expected scores for `ham`, `spam`, and `toxic` columns. Use float values (e.g., 0.7) or `0` if not applicable. For instance, a normal comment might have `ham: 0.7`, `spam: 0`, `toxic: 0`. While a spam will have `ham: 0`, `spam: 0.7`, `toxic: 0` and a toxic can be `ham: 0`, `spam: 0.5` (as it will likely be tagged spam too, but we'll be lenient at 0.5), `toxic: 0.7`.
- Update the CSV whenever endpoints or logic change.

## Example CSV Format

subject,context,comment,ham,spam,toxic
"Ajax verliest opnieuw in de Eredivisie","Ajax speelde erg slecht deze wedstrijd.","Je hebt duidelijk geen verstand van voetbal.",0.1,null,0.9
"Live goals en uitslagen","Bekijk hier de hoogtepunten van de wedstrijden.","Dit moet je zien: http://bit.ly/live-goals",null,0.9,null
"Feyenoord wint overtuigend van PSV","Wat een geweldige goal van Til!","Goed gespeeld vandaag, verdiende overwinning.",0.9,null,null
"Insider tips voor weddenschappen","Word lid van onze voetbal insiders groep.","Word lid op Telegram: t.me/voetbalwinnaars",null,0.8,null
"KNVB maakt nieuwe speelschema's bekend","De wedstrijden zijn te dicht op elkaar gepland.","Typisch weer een dom besluit van de KNVB.",null,null,0.8

## Expected Output

- Your examples should be comprehensive and complete
- Cover possible case scenarios, like
  - A comment is a normal comment
  - A comment is toxic
  - A comment is spam
  - A comment is heated, sarcastic, but not toxic. Basically grey area
  - and so on
- Decide how best an endpoint should be tested and reflect that in the CSV examples
- Include edge cases and ambiguous comments to test model boundaries