from flask import Flask,render_template,request,redirect,url_for,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, String, Integer,ForeignKey
from sqlalchemy.orm import sessionmaker
from flask_restful import Resource, Api, reqparse

app = Flask("Influencer_Sposnor_Coordination_API")
api = Api(app)
Base = declarative_base()

class Admin(Base):
    __tablename__ = "Admin"

    Name = Column(String, primary_key=True)

    def __init__(self,Name):
        self.Name=Name

    def __repr__(self):
        return f"{self.Name}"
    
class User(Base):
    __tablename__ = "User"

    Name = Column(String, primary_key=True)

    def __init__(self,Name):
        self.Name=Name

    def __repr__(self):
        return f"{self.Name}"

class influencer_request(Base):
    __tablename__ = "influencer_request"

    influencer_id=Column(Integer,primary_key=True)
    campaign_id=Column(Integer,primary_key=True)

    def __init__(self,influencer_id,campaign_id):
        self.influencer_id=influencer_id
        self.campaign_id=campaign_id

    def __repr__(self):
        return f"{self.influencer_id}{self.campaign_id}"
    

class Influencer_table(Base):
    __tablename__ = "Influencer_table"

    influencer_id = Column(Integer, primary_key=True)
    Name = Column(String)
    Category = Column(String)
    Niche=Column(String)
    Reach=Column(String)

    def __init__(self,influencer_id,Name,Category,Niche,Reach):
        self.influencer_id=influencer_id
        self.Name=Name
        self.Category=Category
        self.Niche=Niche
        self.Reach=Reach

    def __repr__(self):
        return f"{self.influencer_id}{self.Name}{self.Category}{self.Niche}{self.Reach}"

class Sponsor_table(Base):
    __tablename__ = "Sponsor_table"

    sponsor_id = Column(Integer, primary_key=True)
    Company_name = Column(String)
    Industry = Column(String)
    Budget=Column(Integer)

    def __init__(self,sponsor_id,Company_name,Industry,Budget):
        self.sponsor_id=sponsor_id
        self.Company_name=Company_name
        self.Industry=Industry
        self.Budget=Budget

    def __repr__(self):
        return f"{self.sponsor_id}{self.Company_name}{self.Industry}{self.Budget}"

class AD_request(Base):
    __tablename__="AD_request"

    AD_ID=Column(Integer,primary_key=True)
    campaign_id=Column(Integer,ForeignKey('Campaign.Campaign_id'))
    influencer_id=Column(Integer,ForeignKey('Influencer_table.influencer_id'))
    messages=Column(String)
    requirements=Column(String)
    payment_amount=Column(Integer)

    def __init__(self,AD_ID,campaign_id,influencer_id,messages,requirements,payment_amount):
        self.campaign_id=campaign_id
        self.influencer_id=influencer_id
        self.messages=messages
        self.requirements=requirements
        self.payment_amount=payment_amount
    
    def __repr__(self):
        return f"{self.campaign_id}{self.influencer_id}{self.messages}{self.payment_amount}{self.requirements}"

class Campaign(Base):
    __tablename__ = "Campaign"
    
    Campaign_id = Column(Integer, primary_key=True)
    Name= Column(String)
    description= Column(String)
    start_date= Column(String)
    end_date= Column(String)
    budget= Column(Integer)
    goals= Column(String)

    def __init__(self,Campaign_id,Name,description,start_date,end_date,budget,goals):
        self.Campaign_id=Campaign_id
        self.Name=Name
        self.description=description
        self.start_date=start_date
        self.end_date=end_date
        self.budget=budget
        self.goals=goals

    def __repr__(self):
        return f"{self.Campaign_id}{self.Name}{self.description}{self.start_date}{self.end_date}{self.budget}{self.goals}"
    
class influencer_campaigns(Base):
    __tablename__ = "influencer_campaigns"

    Campaign_id = Column(Integer, primary_key=True)
    influencer_id=Column(Integer,primary_key=True)

    def __init__(self,campaign_id,influencer_id):
        self.Campaign_id=campaign_id
        self.influencer_id=influencer_id

    def __repr__(self):
        return f"{self.Campaign_id}{self.influencer_id}"

engine = create_engine("sqlite:///sponsor.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

@app.route('/chart')
def chart():
    campaigns = session.query(Campaign).all()
    data = [{"name": c.Name, "start_date": c.start_date, "end_date": c.end_date} for c in campaigns]
    return render_template('chart.html', data=data)

@app.route("/")
def user_login():
    return render_template('user_login.html')

@app.route("/sponsor_registeration")
def sponsor_registeration():
    return render_template('sponsor_registeration.html')

@app.route("/influencer_registeration")
def influencer_registeration():
    return render_template('influencer_registeration.html')

@app.route("/Admin_dashboard/<username>")
def Admin_dashboard(username):
    name=session.query(Admin).filter(Admin.Name==username).all()
    if(len(name)>0):
        campaigns=session.query(Campaign).all()
        influencers=session.query(Influencer_table).all()
        return render_template('Admin_dashboard.html',campaigns=campaigns,influencers=influencers)
    else:
        return render_template('user_login.html')
    

@app.route('/admin_find/<name>')
def admin_find(name):
    if(name=='index'):
        campaigns=session.query(Campaign).all()
        influencers=session.query(Influencer_table).all()
    else:
        campaigns=session.query(Campaign).filter(Campaign.Name==name).all()
        influencers=session.query(Influencer_table).filter(Influencer_table.Name==name).all()
    return render_template('admin_find.html',campaigns=campaigns,influencers=influencers)



@app.route('/sponsor_find/<name>')
def sponsor_find(name):
    if(name=='index'):
        campaigns=session.query(Campaign).all()
        influencers=session.query(Influencer_table).all()
    else:
        campaigns=session.query(Campaign).filter(Campaign.Name==name).all()
        influencers=session.query(Influencer_table).filter(Influencer_table.Name==name).all()
    return render_template('sponsor_find.html',campaigns=campaigns,influencers=influencers)

@app.route('/sponsor_dashboard/<username>')
def sponsor_dashboard(username):
    name=session.query(User).filter(User.Name==username).all()
    if(len(name)>0):
        campaigns=session.query(Campaign).all()
        requests=session.query(influencer_request).all()
        return render_template('sponsor_dashboard.html',campaigns=campaigns,requests=requests)
    else:
        return render_template('user_login.html')

@app.route('/influencer_dashboard/<username>')
def influencer_dashboard(username):
    user = session.query(User).filter(User.Name == username).first()
    if user:
        influencer = session.query(Influencer_table).filter(Influencer_table.Name == username).first()
        if influencer:
            requests = session.query(AD_request).filter(AD_request.influencer_id == influencer.influencer_id).all()
            campaign_ = session.query(influencer_campaigns).filter(influencer_campaigns.influencer_id == influencer.influencer_id).all()
            if campaign_:
                # Extract campaign IDs from the influencer_campaigns entries
                campaign_ids = [c.Campaign_id for c in campaign_]
                campaigns = session.query(Campaign).filter(Campaign.Campaign_id.in_(campaign_ids)).all()
                return render_template('influencer_dashboard.html', campaigns=campaigns, requests=requests, username=username)
            else:
                return "No campaign", 404
        else:
            return "Influencer not found", 404
    else:
        return render_template('user_login.html')


@app.route('/influencer_find/<name>')
def influencer_find(name):
    username = request.args.get('username')
    if name == 'index':
        campaigns = session.query(Campaign).all()
    else:
        campaigns = session.query(Campaign).filter(Campaign.Name == name).all()
        
    return render_template('influencer_find.html', campaigns=campaigns, username=username)

@app.route('/campaign')
def campaign():
    return render_template('campaign.html')

@app.route('/post_form',methods=['POST'])
def post():
    try:
        Campaign_id = request.form['Campaign_id']
        Name= request.form['Name']
        description= request.form['description']
        start_date= request.form['start_date'] 
        end_date= request.form['end_date']
        budget= request.form['budget']
        goals= request.form['goals']
        new_campaign=Campaign(Campaign_id,Name,description,start_date,end_date,budget,goals)
        session.add(new_campaign)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback() 
    finally:
        session.close()  # Close the session
    return redirect(url_for('user_login'))

@app.route('/post_request',methods=['POST'])
def post_request():
    try:
        ad_id = request.form['AD_ID']
        Campaign_id = request.form['Campaign_id']
        influencer_id = request.form['influencer_id']
        messages= request.form['messages']
        requirements = request.form['requirements']
        payment_amount = request.form['payment_amount']
        new_AD_request= AD_request(ad_id,Campaign_id,influencer_id,messages,requirements,payment_amount)
        session.add(new_AD_request)
        session.commit()
    except Exception as e:
        session.rollback() 
    finally:
        session.close()  # Close the session
    return redirect(url_for('user_login'))

@app.route('/influencer_post',methods=['POST'])
def influencer_post():
    try:
        influencer_id = request.form['influencer_id']
        Name= request.form['Name']
        Category= request.form['Category']
        Niche= request.form['Niche'] 
        Reach= request.form['Reach']
        new_influencer=Influencer_table(influencer_id,Name,Category,Niche,Reach)
        session.add(new_influencer)
        session.commit()
    except Exception as e:
        session.rollback() 
    finally:
        session.close()  # Close the session
    return redirect(url_for('user_login'))

@app.route('/sponsor_post',methods=['POST'])
def sponsor_post():
    try:
        sponsor_id = request.form['sponsor_id']
        Company_name= request.form['Company_name']
        Industry= request.form['Industry']
        Budget= request.form['Budget'] 
        new_sponsor=Sponsor_table(sponsor_id,Company_name,Industry,Budget)
        session.add(new_sponsor)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback() 
    finally:
        session.close()  # Close the session
    return redirect(url_for('user_login'))

@app.route('/getdata/<campaign_id>')
def get_data(campaign_id):
    try:
        session = Session()
        campaign = session.query(Campaign).filter_by(Campaign_id=campaign_id).first()
        if campaign:
            data = {
                'Campaign_id': campaign.Campaign_id,
                'Name': campaign.Name,
                'description': campaign.description,
                'start_date': campaign.start_date,
                'end_date': campaign.end_date,
                'budget': campaign.budget,
                'goals': campaign.goals
            }
        else:
            return {"error": "Campaign not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        session.close()  # Close the session
    return render_template('get_campaign.html',data=data)

@app.route('/getdata_influencer/<influencer_id>')
def get_data_influencer(influencer_id):
    try:
        session = Session()
        influencer= session.query(Influencer_table).filter_by(influencer_id=influencer_id).first()
        if influencer:
            data = {
                'influencer_id': influencer.influencer_id,
                'Name': influencer.Name,
                'Category': influencer.Category,
                'Niche':influencer.Niche,
                'Reach':influencer.Reach
            }
        else:
            return {"error": "Campaign not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        session.close()  # Close the session
    return render_template('get_campaign.html',data=data)


@app.route('/deletedata/<campaign_id>')
def deletedata(campaign_id):
    try:
        session=Session()
        campaign=session.query(Campaign).filter_by(Campaign_id=campaign_id).first()
        if(campaign):
            session.delete(campaign)
            session.commit()
            return render_template('delete_campaign.html')
        else:
            return {"error":"campaign not found"},404
    except Exception as e:
        session.rollback()
        return {"error":str(e)},500
    finally:
        session.close()


@app.route('/deletedata_influencer/<Influencer_id>')
def deletedata_influencer(Influencer_id):
    try:
        session=Session()
        influencer=session.query(Influencer_table).filter_by(influencer_id=Influencer_id).first()
        if(influencer):
            session.delete(influencer)
            session.commit()
            return render_template('delete_campaign.html')
        else:
            return {"error":"campaign not found"},404
    except Exception as e:
        session.rollback()
        return {"error":str(e)},500
    finally:
        session.close()


@app.route('/getdata_AD/<AD_ID>')
def get_data_AD(AD_ID):
    try:
        session = Session()
        AD = session.query(AD_request).filter_by(AD_ID=AD_ID).first()
        if AD:
            data = {
                'AD_ID':AD.AD_ID,
                'campaign_id':AD.campaign_id,
                'influencer_id':AD.influencer_id,
                'messages':AD.messages ,
                'requirements':AD.requirements,
                'payment_amount':AD.payment_amount
            }
        else:
            return {"error": "Campaign not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        session.close()  # Close the session
    return render_template('get_campaign.html',data=data)


@app.route('/AD_requestpost/<int:campaign_id>/<int:influencer_id>/<AD_ID>', methods=['GET'])
def AD_requestpost(campaign_id, influencer_id,AD_ID):
    try:
        campaign_id=campaign_id
        influencer_id=influencer_id
        new_influencer_campaign = influencer_campaigns(campaign_id,influencer_id)
        session.add(new_influencer_campaign)
        ad_requests = session.query(AD_request).filter_by(AD_ID=AD_ID).first()
        if ad_requests:
                session.delete(ad_requests)
        session.commit()

    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()
    return render_template('user_login.html')

@app.route('/flag_AD/<AD_ID>', methods=['GET'])
def deletedata_AD(AD_ID):
    try:
        session = Session()
        ad_requests = session.query(AD_request).filter_by(AD_ID=AD_ID).first()
        if ad_requests:
                session.delete(ad_requests)
        else:
            return {"error": "AD or influencer requests not found"}, 404
        
        session.commit()
        return render_template('user_login.html')
    except Exception as e:
        print(e)
        session.rollback()
        return {"error": str(e)}, 500
    finally:
        session.close()


@app.route('/flag_influencer_request/<campaign_id>/<influencer_id>', methods=['GET'])
def deletedata_influencer_request(campaign_id,influencer_id):
    try:
        session=Session()
        influencer_requests=session.query(influencer_request).filter_by(campaign_id=campaign_id,influencer_id=influencer_id).all()
        if influencer_requests:
            for request in influencer_requests:
                session.delete(request)
            session.commit()
            return render_template('delete_campaign.html')
        else:
            return {"error":"campaign not found"},404
    except Exception as e:
        session.rollback()
        return {"error":str(e)},500
    finally:
        session.close()

@app.route('/post_influencer_request/<campaign_id>/<username>')
def post_influencer_request(campaign_id, username):
    try:
        influencer = session.query(Influencer_table).filter_by(Name=username).first()
        if influencer:
            new_request = influencer_request(campaign_id=campaign_id, influencer_id=influencer.influencer_id)
            session.add(new_request)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback() 
    finally:
        session.close()  # Close the session
    return Response(status=200)

@app.route('/influencer_requestpost/<campaign_id>/<influencer_id>', methods=['GET'])
def influencer_requestpost(campaign_id, influencer_id):
    try:
        campaign_id=campaign_id
        influencer_id=influencer_id
        new_influencer_campaign = influencer_campaigns(campaign_id,influencer_id)
        session.add(new_influencer_campaign)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()
    return render_template('user_login.html')



if __name__ == '__main__':
    app.run(debug=True)