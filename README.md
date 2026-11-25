# trendpulse

CLI que muestra las tendencias del momento de Google Trends y Hacker News, ordenadas por impacto y limitadas a N resultados. Sin dependencias, solo Python 3.

## Uso

```bash
python3 trendpulse.py --source all -N 10
python3 trendpulse.py --source google --geo MX -N 5
python3 trendpulse.py --source hn -N 20 --json
```

| Opción | Descripción |
|---|---|
| `--source` | `google`, `hn` o `all` (por defecto `all`) |
| `-N`, `--limit` | Número de resultados (por defecto 10) |
| `--geo` | País para Google Trends, código de dos letras (por defecto `MX`) |
| `--json` | Salida en JSON |

## Cómo se ordena

Cada fuente usa su propia métrica real: búsquedas aproximadas en Google Trends y puntos en Hacker News. Dentro de cada fuente se normaliza al valor máximo (0 a 1) para poder mezclarlas en un solo ranking.

## Fuentes y límites

- Google Trends: feed RSS público de tendencias diarias. Google no documenta este endpoint, así que puede cambiar.
- Hacker News: API pública oficial.
- No incluye TikTok ni X: scrapearlos o usar APIs no oficiales va contra sus términos de uso.

## Tests

```bash
python3 test_trendpulse.py
```
