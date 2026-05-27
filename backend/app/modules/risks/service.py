import json
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.contracts.models import Contract
from app.modules.risks.models import RiskItem
from app.modules.reports.models import ReviewReport
from app.llm.deepseek import DeepSeekClient
from app.llm.prompts import REVIEW_SYSTEM_PROMPT


async def run_review(db: AsyncSession, contract: Contract):
    contract.status = "reviewing"
    await db.commit()

    try:
        client = DeepSeekClient()
        result_text = await client.chat([
            {"role": "system", "content": REVIEW_SYSTEM_PROMPT},
            {"role": "user", "content": f"请审查以下合同：\n\n{contract.raw_text}"},
        ])

        # Clean up markdown code fences if present
        result_text = result_text.strip()
        if result_text.startswith("```"):
            result_text = result_text.strip("`").strip()
            if result_text.startswith("json"):
                result_text = result_text[4:].strip()

        data = json.loads(result_text)

        # Save risk items
        for r in data.get("risks", []):
            item = RiskItem(
                contract_id=contract.id,
                clause_index=r.get("clause_index", 0),
                clause_text=r.get("clause_text", ""),
                risk_level=r.get("risk_level", "low"),
                category=r.get("category", ""),
                description=r.get("description", ""),
                legal_basis=r.get("legal_basis", ""),
                suggestion=r.get("suggestion", ""),
            )
            db.add(item)

        # Update contract with review results
        contract.compliance_score = data.get("compliance_score")
        contract.conclusion = data.get("conclusion", "")
        contract.status = "completed"
        contract.reviewed_at = datetime.now(timezone.utc)

        # Determine overall risk level
        risk_levels = [r.get("risk_level") for r in data.get("risks", [])]
        if "high" in risk_levels:
            contract.risk_level = "high"
        elif "medium" in risk_levels:
            contract.risk_level = "medium"
        else:
            contract.risk_level = "low"

        # Save report
        report = ReviewReport(
            contract_id=contract.id,
            report_data=data,
            report_number=f"CR-{contract.id:06d}",
        )
        db.add(report)
        await db.commit()

    except Exception as e:
        contract.status = "failed"
        await db.commit()
        raise e
