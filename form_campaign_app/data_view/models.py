from form_campaign_app import db
from datetime import datetime

class Campaign(db.Model):
    __tablename__ = 'campaign'

    table_id = db.Column(db.Integer, primary_key=True)
    responden_id = db.Column(db.String(50), nullable=False)
    entry_time = db.Column(db.DateTime, default=datetime.utcnow)
    responden_name = db.Column(db.String(100))
    campaign_name = db.Column(db.String(100))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    unit = db.Column(db.String(50))
    brand = db.Column(db.String(50))
    program = db.Column(db.String(100))
    jenis_paket = db.Column(db.String(50))
    nilai_paket = db.Column(db.Float)
    revenue_prorate = db.Column(db.Text)
    total_real_cost = db.Column(db.Float)
    breakdown_cost = db.Column(db.Text)
    breakdown_kpi = db.Column(db.Text)
    activity_type = db.Column(db.Text)
    list_benefit = db.Column(db.Text)
    detail_brief = db.Column(db.Text)
    timeline_benefit = db.Column(db.Text)
    product_knowledge = db.Column(db.String(5))
    key_visual_design = db.Column(db.String(5))

    def to_dict(self):
        return {
            'table_id': self.table_id,
            'responden_id': self.responden_id,
            'entry_time': self.entry_time.strftime('%Y-%m-%d %H:%M:%S'),
            'responden_name': self.responden_name,
            'campaign_name': self.campaign_name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'unit': self.unit,
            'brand': self.brand,
            'program': self.program,
            'jenis_paket': self.jenis_paket,
            'nilai_paket': self.nilai_paket,
            'revenue_prorate': self.revenue_prorate,
            'total_real_cost': self.total_real_cost,
            'breakdown_cost': self.breakdown_cost,
            'breakdown_kpi': self.breakdown_kpi,
            'activity_type': self.activity_type,
            'list_benefit': self.list_benefit,
            'detail_brief': self.detail_brief,
            'timeline_benefit': self.timeline_benefit,
            'product_knowledge': self.product_knowledge,
            'key_visual_design': self.key_visual_design
        } 