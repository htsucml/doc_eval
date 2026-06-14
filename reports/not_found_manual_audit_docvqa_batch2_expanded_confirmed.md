# Expanded Manual NOT_FOUND Audit — DocVQA Batch 2
## Summary
- Input images in uploaded batch: 20
- Exact visual/hash groups used after deduplication: 13
- Confirmed absent-field rows: 65
- Expansion policy: one representative page per exact duplicate group; up to five visually verified absent-field questions per representative.
- Evidence type: assistant visual manual audit, pending user spot-check. No OCR/source-field inventory was used.

## Caveats
- This is more realistic than controlled rendered documents, but less mechanically auditable than synthetic documents with known field dictionaries.
- Duplicate or repeated DocVQA pages were grouped by exact image SHA256 and only representatives were expanded.
- The user should spot-check before final submission and downgrade any suspicious row to `uncertain_illegible` or remove it.

## Duplicate groups
- `batch2-exact-02` representative `docvqa_1e4346b310ff5415.png`; excluded duplicates: docvqa_2032f9ea62254d3b.png, docvqa_3edf3964eeb54e75.png
- `batch2-exact-04` representative `docvqa_207bd1e223307ba6.png`; excluded duplicates: docvqa_5c30703941531d96.png
- `batch2-exact-06` representative `docvqa_2594de3217d7478c.png`; excluded duplicates: docvqa_491c4e868e53fe2d.png, docvqa_5cd4d3c9186d9c68.png
- `batch2-exact-08` representative `docvqa_3717d1d2970205a2.png`; excluded duplicates: docvqa_4a20ada40f0db240.png
- `batch2-exact-09` representative `docvqa_386f5e62fc5fa22f.png`; excluded duplicates: docvqa_4dab7f68490852a6.png

## Confirmed rows

### `docvqa_1e4095752ef28a82.png` — progress_report_projects_table
- duplicate_group: `batch2-exact-01`, group_size=1
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the progress report projects table.
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the progress report projects table.
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the progress report projects table. The page contains client contact phone/email information, but no number is labeled as fax.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the progress report projects table.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the progress report projects table.

### `docvqa_1e4346b310ff5415.png` — corporate_governance_report_page
- duplicate_group: `batch2-exact-02`, group_size=3
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the corporate governance report page.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the corporate governance report page.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the corporate governance report page.
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the corporate governance report page.
- **What is the discount code?** → `discount_code` — No “Discount”, “Promo”, “Coupon”, or discount-code-like field is visible on the corporate governance report page.

### `docvqa_1f1a68084f41940a.png` — invoice_letter
- duplicate_group: `batch2-exact-03`, group_size=1
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the invoice letter.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the invoice letter.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the invoice letter.
- **What is the discount code?** → `discount_code` — No “Discount”, “Promo”, “Coupon”, or discount-code-like field is visible on the invoice letter.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the invoice letter. The letter asks payment to be remitted as soon as possible, but no concrete due-date field is visible.

### `docvqa_207bd1e223307ba6.png` — corporate_governance_committee_table
- duplicate_group: `batch2-exact-04`, group_size=2
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the corporate governance committee-report page.
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the corporate governance committee-report page.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the corporate governance committee-report page.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the corporate governance committee-report page.
- **What is the discount code?** → `discount_code` — No “Discount”, “Promo”, “Coupon”, or discount-code-like field is visible on the corporate governance committee-report page.

### `docvqa_2564e63028039073.png` — workshop_title_page
- duplicate_group: `batch2-exact-05`, group_size=1
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the workshop title page.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the workshop title page.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the workshop title page.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the workshop title page.
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the workshop title page.

### `docvqa_2594de3217d7478c.png` — annual_report_brand_article
- duplicate_group: `batch2-exact-06`, group_size=3
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the annual report brand-article page.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the annual report brand-article page.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the annual report brand-article page.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the annual report brand-article page.
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the annual report brand-article page.

### `docvqa_321ebde4ec0aa3e6.png` — temporary_payment_detail_report
- duplicate_group: `batch2-exact-07`, group_size=1
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the temporary payment detail report.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the temporary payment detail report.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the temporary payment detail report.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the temporary payment detail report. The description contains an abbreviated product/shipping-related note, but no carrier or explicit shipping-method field is visible.
- **What is the discount code?** → `discount_code` — No “Discount”, “Promo”, “Coupon”, or discount-code-like field is visible on the temporary payment detail report.

### `docvqa_3717d1d2970205a2.png` — phone_message_slip
- duplicate_group: `batch2-exact-08`, group_size=2
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the phone message slip. The slip contains a telephone/message context, but no number is labeled as fax.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the phone message slip.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the phone message slip.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the phone message slip.
- **What is the discount code?** → `discount_code` — No “Discount”, “Promo”, “Coupon”, or discount-code-like field is visible on the phone message slip.

### `docvqa_386f5e62fc5fa22f.png` — budget_expense_form
- duplicate_group: `batch2-exact-09`, group_size=2
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the budget expense form.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the budget expense form.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the budget expense form.
- **What is the tracking number?** → `tracking_number` — No tracking number or carrier tracking field is visible on the budget expense form.
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the budget expense form.

### `docvqa_3e69015b39175e87.png` — environment_survey_table
- duplicate_group: `batch2-exact-10`, group_size=1
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the environment survey table page.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the environment survey table page.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the environment survey table page.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the environment survey table page.
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the environment survey table page.

### `docvqa_404ce70b9d2c333f.png` — report_foreword_scan
- duplicate_group: `batch2-exact-11`, group_size=1
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the report foreword scan. The visible foreword text is faint but legible enough to see no fax-labeled field.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the report foreword scan.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the report foreword scan.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the report foreword scan.
- **What is the discount code?** → `discount_code` — No “Discount”, “Promo”, “Coupon”, or discount-code-like field is visible on the report foreword scan.

### `docvqa_42b812fca2de2f23.png` — balance_sheet_schedule_table
- duplicate_group: `batch2-exact-12`, group_size=1
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the balance-sheet schedule table.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the balance-sheet schedule table.
- **What is the payment due date?** → `payment_due_date` — No payment due date or due-date field is visible on the balance-sheet schedule table.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the balance-sheet schedule table.
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the balance-sheet schedule table.

### `docvqa_55db519ade867e34.png` — budget_request_summary_form
- duplicate_group: `batch2-exact-13`, group_size=1
- **What is the fax number?** → `fax_number` — No “Fax” or “Facsimile” label and no fax-labeled phone number is visible on the budget request summary form.
- **What is the shipping method?** → `shipping_method` — No “Shipping method”, “Ship via”, carrier, or delivery-method field is visible on the budget request summary form.
- **What is the vendor tax ID?** → `vendor_tax_id` — No “Vendor Tax ID”, “Tax ID”, “TIN”, or tax-identification field is visible on the budget request summary form.
- **What is the discount code?** → `discount_code` — No “Discount”, “Promo”, “Coupon”, or discount-code-like field is visible on the budget request summary form.
- **What is the purchase order number?** → `purchase_order_number` — No purchase order number, PO number, or purchase-order field is visible on the budget request summary form. The form contains budget/grant fields, but no PO-number or purchase-order field is visible.
