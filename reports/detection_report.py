import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


class DetectionReportGenerator:
    """Generates professional cybersecurity audit PDF reports for profile analyses."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._init_custom_styles()

    def _init_custom_styles(self):
        self.title_style = ParagraphStyle(
            'ReportTitle',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=6,
        )
        self.subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#64748B'),
            spaceAfter=12,
        )
        self.section_heading = ParagraphStyle(
            'SectionHeading',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=10,
            spaceAfter=6,
        )
        self.body_style = ParagraphStyle(
            'ReportBody',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor('#334155'),
        )
        self.body_bold = ParagraphStyle(
            'ReportBodyBold',
            parent=self.body_style,
            fontName='Helvetica-Bold',
        )
        self.disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=self.styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#64748B'),
        )

    def generate(self, data: dict, output_stream: io.BytesIO = None) -> io.BytesIO:
        """
        Builds the PDF report from the provided detection data dictionary.
        """
        if output_stream is None:
            output_stream = io.BytesIO()

        doc = SimpleDocTemplate(
            output_stream,
            pagesize=letter,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        story = []

        # Header Banner
        header_data = [
            [
                Paragraph("<b>FAKE PROFILE DETECTION SYSTEM</b><br/><font size='8' color='#94A3B8'>CYBERSECURITY AUDIT &amp; FORENSIC INTELLIGENCE</font>", self.title_style),
                Paragraph(f"<b>Report ID:</b> #{data.get('id', 'N/A')}<br/><b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}<br/><b>Status:</b> AUDIT VERIFIED", self.body_style)
            ]
        ]
        header_table = Table(header_data, colWidths=[4.0 * inch, 3.2 * inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        story.append(header_table)
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3B82F6'), spaceBefore=8, spaceAfter=14))

        # Executive Verdict Box
        risk_level = data.get('risk_level', 'Medium').upper()
        if risk_level == 'HIGH':
            badge_bg = colors.HexColor('#FEE2E2')
            badge_text = colors.HexColor('#991B1B')
            badge_border = colors.HexColor('#EF4444')
        elif risk_level == 'MEDIUM':
            badge_bg = colors.HexColor('#FEF3C7')
            badge_text = colors.HexColor('#92400E')
            badge_border = colors.HexColor('#F59E0B')
        else:
            badge_bg = colors.HexColor('#D1FAE5')
            badge_text = colors.HexColor('#065F46')
            badge_border = colors.HexColor('#10B981')

        verdict_data = [
            [
                Paragraph(f"<b>TARGET ACCOUNT:</b> @{data.get('username', 'unknown')}<br/>"
                          f"<b>FINAL VERDICT:</b> {data.get('final_verdict', 'Under Review')}<br/>"
                          f"<b>COMBINED RISK SCORE:</b> {data.get('overall_risk_score', 0):.1f} / 100", self.body_style),
                Paragraph(f"<font size='14'><b>RISK LEVEL</b></font><br/><font size='18'><b>{risk_level}</b></font>", 
                          ParagraphStyle('RiskBadge', parent=self.title_style, alignment=1, textColor=badge_text))
            ]
        ]
        verdict_table = Table(verdict_data, colWidths=[4.8 * inch, 2.4 * inch])
        verdict_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), badge_bg),
            ('BOX', (0, 0), (-1, -1), 1.5, badge_border),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(verdict_table)
        story.append(Spacer(1, 14))

        # Target Profile Metadata
        story.append(Paragraph("1. Target Profile Attributes", self.section_heading))
        meta_table_data = [
            [
                Paragraph("<b>Followers:</b>", self.body_style), str(data.get('followers_count', 0)),
                Paragraph("<b>Following:</b>", self.body_style), str(data.get('following_count', 0)),
                Paragraph("<b>Posts:</b>", self.body_style), str(data.get('posts_count', 0)),
            ],
            [
                Paragraph("<b>Account Age:</b>", self.body_style), f"{data.get('account_age_days', 0)} days",
                Paragraph("<b>Bio Length:</b>", self.body_style), f"{data.get('bio_length', 0)} chars",
                Paragraph("<b>Has Profile Pic:</b>", self.body_style), "Yes" if data.get('has_profile_pic') else "No",
            ],
            [
                Paragraph("<b>Verified Status:</b>", self.body_style), "Verified" if data.get('is_verified') else "Unverified",
                Paragraph("<b>Avg Likes:</b>", self.body_style), str(data.get('avg_likes', 0.0)),
                Paragraph("<b>Avg Comments:</b>", self.body_style), str(data.get('avg_comments', 0.0)),
            ]
        ]
        meta_table = Table(meta_table_data, colWidths=[1.3 * inch, 1.1 * inch, 1.3 * inch, 1.1 * inch, 1.3 * inch, 1.1 * inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 14))

        # Dual Engine Evidence Breakdown
        story.append(Paragraph("2. Dual-Engine Intelligence Breakdown", self.section_heading))
        
        ml_score = data.get('ml_fake_probability', 0.0) * 100
        onto_score = data.get('ontology_risk_score', 0.0)
        
        engines_data = [
            [
                Paragraph("<b>Machine Learning Model (Random Forest)</b>", self.body_bold),
                Paragraph("<b>Semantic Ontology Engine (OWL/RDF)</b>", self.body_bold)
            ],
            [
                Paragraph(
                    f"• <b>Prediction:</b> {data.get('ml_prediction', 'N/A')}<br/>"
                    f"• <b>Fake Probability:</b> {ml_score:.1f}%<br/>"
                    f"• <b>Confidence Score:</b> {data.get('ml_confidence', 0.0):.1f}%<br/>"
                    f"• <b>Engine Weight:</b> 55% in Hybrid Synthesis", self.body_style
                ),
                Paragraph(
                    f"• <b>Ontology Verdict:</b> {data.get('ontology_verdict', 'N/A')}<br/>"
                    f"• <b>Semantic Risk Score:</b> {onto_score:.1f} / 100<br/>"
                    f"• <b>Inferred Classes:</b> {', '.join(data.get('ontology_inferred_classes', ['SocialMediaProfile']))}<br/>"
                    f"• <b>Engine Weight:</b> 45% in Hybrid Synthesis", self.body_style
                ),
            ]
        ]
        engines_table = Table(engines_data, colWidths=[3.6 * inch, 3.6 * inch])
        engines_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#EDE9FE')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
            ('PADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(engines_table)
        story.append(Spacer(1, 14))

        # Forensic Findings & Triggered Rules
        story.append(Paragraph("3. Forensic Indicators & Semantic Axioms Triggered", self.section_heading))
        reasons = data.get('flagged_reasons', [])
        if not reasons:
            rules_triggered = data.get('ontology_rules_triggered', [])
            reasons = [r.get('description', str(r)) for r in rules_triggered] if rules_triggered else ["No high-risk anomalies or suspicious patterns detected."]

        reasons_data = []
        for idx, reason in enumerate(reasons, 1):
            reasons_data.append([Paragraph(f"<b>[{idx}]</b>", self.body_bold), Paragraph(str(reason), self.body_style)])

        reasons_table = Table(reasons_data, colWidths=[0.5 * inch, 6.7 * inch])
        reasons_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#F1F5F9')),
        ]))
        story.append(reasons_table)
        story.append(Spacer(1, 14))

        # Tactical Security Recommendations
        story.append(Paragraph("4. Recommended Tactical Actions", self.section_heading))
        if risk_level == 'HIGH':
            rec_text = "• <b>Restricted Action:</b> Recommend flagging this account for identity verification challenge or manual moderation review.<br/>• <b>Precaution:</b> Do not conduct direct financial transactions or share sensitive credentials with this account.<br/>• <b>Network Impact:</b> Block account to mitigate automated bot propagation."
        elif risk_level == 'MEDIUM':
            rec_text = "• <b>Elevated Monitoring:</b> Flag account for behavioral monitoring. Account exhibits suspicious ratio or activity patterns.<br/>• <b>Verification:</b> Request secondary identity proof if engaging in sponsored collaboration or commerce."
        else:
            rec_text = "• <b>Standard Trust:</b> Account metrics adhere to normal organic user behavioral baselines.<br/>• <b>Routine Audit:</b> No immediate defensive measures required."

        rec_table = Table([[Paragraph(rec_text, self.body_style)]], colWidths=[7.2 * inch])
        rec_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(rec_table)
        story.append(Spacer(1, 16))

        # Forensic Audit Disclaimer
        story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#E2E8F0'), spaceBefore=8, spaceAfter=8))
        disclaimer_text = (
            "<b>Forensic AI Intelligence Disclaimer:</b> This report is generated through an automated hybrid analysis "
            "synthesizing Scikit-Learn Machine Learning probabilistic models and OWL 2 Semantic Web Ontological reasoning rules. "
            "Suspicious indicators and probabilistic risk scores represent heuristic vulnerability indicators and do not constitute "
            "absolute legal proof of identity fraud. Findings are intended for cyber intelligence and risk mitigation decision support."
        )
        story.append(Paragraph(disclaimer_text, self.disclaimer_style))

        doc.build(story)
        output_stream.seek(0)
        return output_stream
