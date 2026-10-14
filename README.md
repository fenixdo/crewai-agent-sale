# crewai-agent-sale

Agent **Sale** trong sample vận hành "Kế hoạch chiến dịch quý" (Marketing · Sale · HR) chạy trên CrewAI AMP.

- Nhận đề xuất chiến dịch (số lead, ngân sách) → dự báo hợp đồng, doanh số sau khuyến mãi, hoa hồng, số nhân viên bán hàng và chỉ tiêu mỗi người.
- Số liệu tính bằng code trong tool `sales_forecast` theo `src/crewai_agent_sale/policy.yaml`. **Đổi chính sách = sửa file này rồi push.**
- Gọi được 2 cách: `/kickoff` của deployment (input `proposal`, JSON) hoặc **A2A** (`/a2a`, agent card ở `/.well-known/agent-card.json`), xác thực `Authorization: Bearer $AUTH_TOKEN`.
- LLM: **FakeLLM** trả lời theo kịch bản (`script.py`) — không cần khóa. Đặt `MODEL=<provider/model>` (+ khóa) để dùng LLM thật.

```bash
uv sync --group dev && .venv/bin/pytest -q      # test offline
.venv/bin/crewai run                            # chạy với dữ liệu mẫu
.venv/bin/crewai deploy validate                # kiểm tra trước deploy
```

`src/crewai_agent_sale/fake_llm.py` được sinh từ `ams/template/` (sửa ở đó rồi chạy `ams/scripts/sync_template.py`).
