"""
A WSGI app with the Flask framework and PyMongo
to provide insigths of BBC-Programmes via
advance search functionality.

@author siddiq.taimur@gmail.com
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_pymongo import PyMongo
import json


app = Flask(__name__)

app.config['MONGO_HOST'] = 'localhost'
app.config['MONGO_PORT']='27017'
app.config['MONGO_DBNAME']="data"


mongo = PyMongo(app,config_prefix='MONGO')

@app.route('/')
def home():
    brands = sorted(mongo.db.bbc_test.distinct('complete_title.brand'))
    series = sorted(mongo.db.bbc_test.distinct('complete_title.series'))
    series_titles = sorted(mongo.db.bbc_test.distinct('complete_title.series_title'))
    episodes = sorted(mongo.db.bbc_test.distinct('complete_title.episode'))
    masterbrands = sorted(mongo.db.bbc_test.distinct('masterbrand'))
    services = sorted(mongo.db.bbc_test.distinct('service'))
    all_categories = sorted(mongo.db.bbc_test.distinct('categories'))
    tags = sorted(mongo.db.bbc_test.distinct('tags'))
    return render_template("home.html",
                            brands=brands, series=series, series_titles=series_titles, episodes=episodes,
                            masterbrands=masterbrands, services=services,
                            categories=all_categories, tags=tags)


@app.route('/all_programmes')
def all_programmes():
    programmes = mongo.db.bbc_test.find({}, {'_id':False, 'brand_pid':False})
    return render_template("programmes.html", foundProgammes=programmes, searchedString = "\"Showing all Programmes\"")

@app.route('/about')
def aboutUs():
    return render_template("aboutus.html")


@app.route('/', methods=["POST"])
def postFormInputs():
        keyword = request.form['keyword']
        brand  = request.form['brand']
        series  = request.form['series']
        series_title  = request.form['series_title']
        episode  = request.form['episode']
        masterbrand  = request.form['masterbrand']
        service  = request.form['service']
        start_date  = request.form['start_date']
        end_date  = request.form['end_date']
        media_type  = request.form['media_type']
        is_clip = request.form['is_clip']
        categories_list = request.form.getlist('categories')
        tags_list = request.form.getlist('tagPicker')
        formInputs = json.dumps({'keyword':keyword, 'brand':brand, 'series':series, 'series_title':series_title,
                        'episode':episode, 'masterbrand':masterbrand, 'service':service, 'start_date':start_date, 'end_date':end_date,
                        'media_type':media_type, 'is_clip':is_clip, 'categories_list':categories_list, 'tags_list':tags_list})
        return redirect(url_for('findingProgrammes', formInputs=formInputs))


@app.route('/found_programmes')
def findingProgrammes():
        formInputs = json.loads(request.args['formInputs'])
        keyword = formInputs['keyword']
        brand  = formInputs['brand']
        series  = formInputs['series']
        series_title  = formInputs['series_title']
        episode  = formInputs['episode']
        masterbrand  = formInputs['masterbrand']
        service  = formInputs['service']
        start_date  = formInputs['start_date']
        end_date  = formInputs['end_date']
        media_type  = formInputs['media_type']
        is_clip = formInputs['is_clip']
        categories_list = formInputs['categories_list']
        tags_list = formInputs['tags_list']

        programmes = [];
        programmes_ids = "";
        searchedString = "";
        # Show all programmes, if everything is default
        if( all(x=='' for x in (keyword, series, series_title, episode, start_date, end_date))
            and all(y=='any' for y in (brand, masterbrand, service, media_type, is_clip))
            and ('all' in categories_list) and ('all' in tags_list) ):
            programmes = mongo.db.bbc_test.find({}, {'_id':False, 'brand_pid':False}) # removing mongo _id and brand_pid
            searchedString = "\"Showing All Programmes\",";
        else:
            keyword = keyword.strip()
            if(keyword!=''):
                searchedString = "Keywords:\""+keyword+"\",";
                programmes_ids = mongo.db.bbc_test.distinct('_id', {'$or':[
                {'complete_title.episode':{'$regex':keyword, '$options':'i'}},
                {'complete_title.series_title':{'$regex':keyword, '$options':'i'}},
                {'complete_title.series':{'$regex':keyword, '$options':'i'}},
                {'complete_title.brand':{'$regex':keyword, '$options':'i'}}
                ]}) # option i is telling about case_insensitive
            if(brand!='any'):
                searchedString = searchedString +" Brand:\""+brand+"\",";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'complete_title.brand':brand.lower(), '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'complete_title.brand':brand.lower()})
            if(series!=''):
                searchedString = searchedString +" Series:\""+series+"\",";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'complete_title.series':series.lower(), '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'complete_title.series':series.lower()})
            if(series_title!=''):
                searchedString = searchedString +" Series_Title:\""+series_title+"\",";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'complete_title.series_title':series_title.lower(), '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'complete_title.series_title':series_title.lower()})
            if(episode!=''):
                searchedString = searchedString +" Episode:\""+episode+"\",";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'complete_title.episode':episode.lower(), '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'complete_title.episode':episode.lower()})
            if(masterbrand!='any'):
                searchedString = searchedString +" Masterbrand:\""+masterbrand+"\",";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'masterbrand':masterbrand.lower(), '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'masterbrand':masterbrand.lower()})
            if(service!='any'):
                searchedString = searchedString +" Service/Channel:\""+service+"\",";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'service':service.lower(), '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'service':service.lower()})
            if(start_date!='' and end_date!=''):
                searchedString = searchedString +" Start_date:\""+start_date+"\"," +" End_date:\""+end_date+"\",";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'epoch_start':{'$gte':start_date}, 'epoch_end':{'$lte':end_date}, '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'epoch_start':{'$gte':start_date}, 'epoch_end':{'$lte':end_date}})
            if(media_type!='any'):
                searchedString = searchedString +" Media_type:\""+media_type+"\",";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'media_type':media_type.lower(), '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'media_type':media_type.lower()})
            if(is_clip!='any'):
                searchedString = searchedString +" Clip:\""+is_clip+"\",";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'is_clip':{'$eq':int(is_clip)}, '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'is_clip':{'$eq':int(is_clip)}})
            if('all' not in categories_list):
                searchedString = searchedString +" Categories:[\""+ "\",\"".join(categories_list) +"\"],";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'categories':{'$in':categories_list}, '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'categories':{'$in':categories_list}})
            if('all' not in tags_list):
                searchedString = searchedString +" Tags:[\""+ "\",\"".join(tags_list) +"\"],";
                if(programmes_ids!=""):
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'tags':{'$in':tags_list}, '_id':{'$in':programmes_ids}})
                else:
                    programmes_ids = mongo.db.bbc_test.distinct('_id', {'tags':{'$in':tags_list}})

        if(programmes_ids!=""):
            programmes = mongo.db.bbc_test.find({'_id':{'$in':programmes_ids}}, {'_id':False, 'brand_pid':False})

        searchedString = searchedString[:-1]; # removing the last , from the string

        return render_template("programmes.html", foundProgammes=programmes, searchedString=searchedString)


if __name__ == '__main__':
    app.run(debug = True)
