from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import tempfile

from app.core.database import get_db
from app.modules.reports.models import ReviewReport
from app.modules.contracts.models import Contract

router = APIRouter(prefix="/api/contracts/{contract_id}/report", tags=["reports"])


@router.get("")
async def get_report(contract_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ReviewReport).where(ReviewReport.contract_id == contract_id))
    report = result.scalar_one_or_none()
    if not report:
        return {"error": "not found"}
    return {
        "id": report.id,
        "contract_id": report.contract_id,
        "report_number": report.report_number,
        "report_data": report.report_data,
        "generated_at": report.generated_at,
    }


@router.post("/export")
async def export_report(contract_id: int, db: AsyncSession = Depends(get_db)):
    from weasyprint import HTML

    result = await db.execute(select(ReviewReport).where(ReviewReport.contract_id == contract_id))
    report = result.scalar_one_or_none()
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    contract = result.scalar_one_or_none()
    if not report or not contract:
        return {"error": "not found"}

    risks = report.report_data.get("risks", [])
    risk_rows = ""
    for r in risks:
        color = {"high": "#dc2626", "medium": "#f59e0b", "low": "#3b82f6"}.get(
            r.get("risk_level", "low"), "#666"
        )
        risk_rows += f"""
        <tr>
            <td style="color:{color};font-weight:bold;">{r.get('risk_level','').upper()}</td>
            <td>{r.get('category','')}</td>
            <td>{r.get('description','')}</td>
            <td>{r.get('suggestion','')}</td>
        </tr>"""

    html_content = f"""<html><meta charset="utf-8"><body>
    <h1 style="text-align:center;">AI 合同审查报告</h1>
    <p><strong>合同名称：</strong>{contract.title}</p>
    <p><strong>报告编号：</strong>{report.report_number}</p>
    <p><strong>生成日期：</strong>{report.generated_at.strftime('%Y-%m-%d')}</p>
    <p><strong>合规评分：</strong>{contract.compliance_score}/100</p>
    <h2>风险清单</h2>
    <table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;">
    <tr><th>风险等级</th><th>类别</th><th>描述</th><th>建议</th></tr>
    {risk_rows}
    </table>
    <h2>审查结论</h2>
    <p>{contract.conclusion or '无'}</p>
    <p style="margin-top:40px;font-size:12px;color:#999;">本报告由 AI 自动生成，仅供内部合规参考。</p>
    </body></html>"""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        HTML(string=html_content).write_pdf(tmp.name)
        return FileResponse(
            tmp.name,
            media_type="application/pdf",
            filename=f"{contract.title}-审查报告.pdf",
        )
