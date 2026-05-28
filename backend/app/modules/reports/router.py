import tempfile
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from fpdf import FPDF
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.contracts.models import Contract
from app.modules.reports.models import ReviewReport

FONT_PATH = "C:/Windows/Fonts/simfang.ttf"    # FangSong (regular, single TTF)
FONT_BOLD = "C:/Windows/Fonts/simhei.ttf"    # SimHei (bold, single TTF)

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


def risk_color(level: str) -> tuple:
    return {
        "high": (220, 38, 38),
        "medium": (245, 158, 11),
        "low": (59, 130, 246),
    }.get(level, (102, 102, 102))


@router.post("/export")
async def export_report(contract_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ReviewReport).where(ReviewReport.contract_id == contract_id))
    report = result.scalar_one_or_none()
    result = await db.execute(select(Contract).where(Contract.id == contract_id))
    contract = result.scalar_one_or_none()
    if not report or not contract:
        return {"error": "not found"}

    risks = report.report_data.get("risks", [])

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.add_font("yh", "", FONT_PATH)
    pdf.add_font("yh_b", "", FONT_BOLD)
    pdf.set_font("yh_b", "", 24)
    pdf.ln(60)
    pdf.cell(0, 15, "AI 合同审查报告", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("yh", "", 12)
    pdf.ln(10)
    report_num = report.report_number or f"CR-{contract.id:06d}"
    pdf.cell(0, 8, f"报告编号：{report_num}", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(0, 8, f"合同名称：{contract.title}", new_x="LMARGIN", new_y="NEXT", align="C")
    date_str = contract.reviewed_at.strftime("%Y-%m-%d") if contract.reviewed_at else datetime.now().strftime("%Y-%m-%d")
    pdf.cell(0, 8, f"审查日期：{date_str}", new_x="LMARGIN", new_y="NEXT", align="C")
    level_label = {"high": "高风险", "medium": "中风险", "low": "低风险"}.get(
        contract.risk_level or "low", "未知"
    )
    pdf.cell(0, 8, f"审查结论：{level_label}", new_x="LMARGIN", new_y="NEXT", align="C")

    # Page 2: Review conclusion
    pdf.add_page()
    pdf.set_font("yh_b", "", 16)
    pdf.cell(0, 12, "审查结论", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("yh", "", 12)
    pdf.ln(4)
    score_color = (22, 163, 74) if (contract.compliance_score or 0) >= 80 else (217, 119, 6) if (contract.compliance_score or 0) >= 60 else (220, 38, 38)
    pdf.set_text_color(*score_color)
    pdf.set_font("yh_b", "", 28)
    pdf.cell(0, 14, f"{contract.compliance_score or '-'} / 100", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("yh", "", 12)
    pdf.ln(4)
    pdf.set_font("yh", "", 11)
    pdf.x = pdf.l_margin
    pdf.multi_cell(0, 6, contract.conclusion or "无")

    # Page 3+: Risk list
    if risks:
        pdf.add_page()
        pdf.set_font("yh_b", "", 16)
        pdf.cell(0, 12, "风险清单", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

        for i, r in enumerate(risks, 1):
            color = risk_color(r.get("risk_level", "low"))
            pdf.set_font("yh_b", "", 11)
            level_map = {"high": "高风险", "medium": "中风险", "low": "低风险"}
            pdf.set_text_color(*color)
            pdf.cell(0, 7, f"{i}. 第{r.get('clause_index', '')}条 · {r.get('category', '')} · {level_map.get(r.get('risk_level', ''), '')}", new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("yh", "", 10)
            pdf.x = pdf.l_margin
            pdf.multi_cell(0, 5.5, f"风险描述：{r.get('description', '')}")
            if r.get("legal_basis"):
                pdf.x = pdf.l_margin
                pdf.multi_cell(0, 5.5, f"法律依据：{r.get('legal_basis', '')}")
            if r.get("suggestion"):
                pdf.set_text_color(146, 64, 14)
                pdf.x = pdf.l_margin
                pdf.multi_cell(0, 5.5, f"修改建议：{r.get('suggestion', '')}")
                pdf.set_text_color(0, 0, 0)
            pdf.ln(3)

    # Last page: Disclaimer
    pdf.add_page()
    pdf.set_font("yh", "", 10)
    pdf.set_text_color(153, 153, 153)
    pdf.ln(40)
    pdf.cell(0, 8, "免责声明", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.x = pdf.l_margin
    pdf.multi_cell(0, 6, "本报告由 AI 自动生成，仅供内部合规参考，不构成法律意见。")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        return FileResponse(
            tmp.name,
            media_type="application/pdf",
            filename=f"{contract.title}-审查报告.pdf",
        )
