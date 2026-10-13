EdgeFinder AI v0.1 — Kalshi public-market explorer

Requires Windows 10/11 and Python 3.10+ installed.
Run START_EDGEFINDER.cmd. The app starts a localhost-only server and
opens a browser tab. Keep the command window open while using it.
No Kalshi credentials, account, trading API or order endpoints are used.

Upstream read-only API:
https://api.elections.kalshi.com/trade-api/v2/markets
Supports pagination, market status filters, prices, volume and liquidity.
Public endpoint availability and field schemas can change. The app reports
API failures rather than displaying fabricated market prices.

FEATURES:
- Read-only live market list; fetches additional pages on demand.
- Search, sort, liquidity/spread inspection, market details/rules.
- Local browser watchlist, CSV export, user-supplied probability calculator.
- All categories are supported as exposed by the markets endpoint, but
  all markets are NOT preloaded automatically; use pagination.
- No automatic prediction model or proven positive-EV detection.
- Fees, execution uncertainty and forecast error excluded from edge display.

SECURITY: Localhost-only server; no API keys. No trading capabilities.
