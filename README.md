# portfolio-analyst
Build on top of Yahoo finance functionality and calculates simple financial metrics for provided tickers.

Collect data on central bank market interventions. Using various statistical techniques evaluate impact of central bank interventions on provided ticker data.

# Get central bank data:
1. ECB asset purchase programme data

curl 'https://www.ecb.europa.eu/mopo/pdf/APP_breakdown_history.csv?fe3f0618390295f6e54b73227e892d96'>>APP_breakdown_history.csv

2. ECB open market operations data

curl 'https://www.ecb.europa.eu/mopo/implement/omo/html/tops_mobu.zip?1335610d7e5530ede67cc62e0441e33a' >> ecp_omo/

3. FED balance sheet data

curl https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=WALCL&scale=left&cosd=2002-12-18&coed=2021-12-22&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Weekly%2C%20As%20of%20Wednesday&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-12-25&revision_date=2021-12-25&nd=2002-12-18 >>'fed.csv'

# TODO:
1. Collect data from other major central banks: BoE, PBoC, CBoJ
2. Implemnt various statistical techniques to asses level of impact on central bank market interventions on financial instrument valuations
