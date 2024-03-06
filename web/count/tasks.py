from myproject.celery import app
from .services import CountBookTicker, AnalysisProfitLinks


@app.task
def count():
    return CountBookTicker().main()


@app.task
def analysis_profit_links():
    return AnalysisProfitLinks().save()