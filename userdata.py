# Copyright (c) 2023, human and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class userdata(Document):
	pass
# /home/apple/frappe-bench/apps/temp_app/

@frappe.whitelist(allow_guest=1)
def user_data(username):
	doc = frappe.new_doc('userdata');
	doc.user_name=username
	doc.insert(ignore_permissions=True);
	doc.save();
	frappe.db.commit();
	dict={}
	dict['user_id']=doc.name

	return dict



@frappe.whitelist(allow_guest=1)
def user_value(user_id,quest_id,value):
# def user_value():
	alldoc=[]
	doc_name=frappe.get_list("userdata")
	for data in doc_name:
		alldoc.append(data['name'])
	if user_id not in alldoc:
		return "User ID is Not Avaliable ....."
	all_quest_id=[]
	all_id=frappe.get_list("ALLQuestions",fields=['uid'])
	for ids in all_id:
		all_quest_id.append(ids['uid'])
	if quest_id not in all_quest_id:
		return "Question ID is Not Avaliable ....."
	options= frappe.get_doc("userdata",user_id)
	optionid=[]
	print(len(options.selected_options))
	for i in range(len(options.selected_options)):
		optionid.append(options.selected_options[i].qid)
	if quest_id not in optionid:
		dummy={}
		dummy[quest_id]=value
		docdata=frappe.get_doc("userdata",user_id)
		opt=docdata.append("selected_options",dummy);
		opt.save();
		frappe.db.commit();
		options.reload()
		options.selected_options[len(options.selected_options)-1].qid=quest_id
		options.selected_options[len(options.selected_options)-1].values=value
		options.save()
		frappe.db.commit();
		options.reload()
		# return options
		omega={}
		omega['name']=options.name;
		omega['user_name']=options.user_name;
		datas={};
		for hu in range(len(options.selected_options)):
			datas[options.selected_options[hu].qid]=options.selected_options[hu].values
		omega['data']=datas
		return omega
	
	return "Question ID Already Exist in User ID"

	

	
