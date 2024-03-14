from flask_restful import Resource, reqparse
from database.queries import DB_Queries
from database.dB_Execute import *
from public.strings.strings import *
from database.queries import *
from src.server.constants.response import *
from datetime import datetime
import pymongo
import requests
from langchain_openai import OpenAI
import os
import re
import smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from transformers import PegasusTokenizer, PegasusForConditionalGeneration, T5Tokenizer, T5ForConditionalGeneration
import torch

api_key = ''   # --- working vv
os.environ['OPENAI_API_KEY'] = api_key
newline = ""



class ProjectEnquiry(Resource):
    def post(self):
        requestData = request.get_json()
        if (not request.get_json()
                or not 'enquiry' in request.get_json()
                or not 'service' in request.get_json()):
            return emptyDataResponse()
        try:
            if(requestData['enquiry'] == 'Project Enquiry' and requestData['service'] == []):
                # getServices = fetchAllWhere(DB_Queries.SelectAllServices)
                getServices = list(services.find())
                if len(getServices)>0:
                    servicesList = []
                    for i in range(len(getServices)):
                        resultJson = {
                            'id' : str(getServices[i]['_id']),
                            'serviceName' : getServices[i]['serviceName'],
                            'isActice' : getServices[i]['isActive'],
                            'URL' : getServices[i]['serviceUrl']
                        }
                        servicesList.append(resultJson)
                    response = {
                            "data" : servicesList,
                            "success" : True
                    }
                else:
                    response = failedResponse()
            elif(requestData['enquiry'] == '' and requestData['service'] != []):
                # getServiceURL = fetchAllWhere(DB_Queries.SelectServiceURL, requestData['enquiry'])
                subServicesList = []
                for i in requestData['service']:
                    getSubServices = list(subservices.find({"serviceName":i}))
                    if len(getSubServices)>0:
                        for j in range(len(getSubServices)):
                            resultJson = {
                                'serviceName' : getSubServices[j]['serviceName'],
                                'subServices' : getSubServices[j]['subServices']
                            }
                            subServicesList.append(resultJson)
                response = {
                        "data" : subServicesList,
                        "success" : True
                }
            else:
                response = emptyDataResponse()
        except Exception as e:
            response = exceptionResponseWithMessage(str(e))
        return response

class SummaryOnRequirements(Resource):
    def post(self):
        requestData = request.get_json()
        if (not request.get_json()
                or not 'userRequirements' in request.get_json() or requestData['userRequirements'] == ''):
            return emptyDataResponse()
        try:
            llm = OpenAI(temperature=1.0)
            # summary = llm("Please provide service details from Terralogic software solutions for" + requestData['userRequirements'] + "as response with warmful respect without mentioning user name.")
            summary = llm("Please provide service details in 2 lines from Terralogic software solutions for" + requestData['userRequirements'] + "as response with warmful respect without mentioning user name.")
            cleanedText = re.sub(r'\\n\d*', '', summary)
            finalResponse = ' '.join([line.strip() for line in cleanedText.split('\n')])
            removedSPace = re.sub(' +', ' ', finalResponse)
            response = {
                'summary' : removedSPace
            }
        except Exception as e:
            response = exceptionResponseWithMessage(str(e))
        return response


# def generate_summary(input_text):
#     # Load T5 model and tokenizer
#     model_name = "t5-base"
#     tokenizer = T5Tokenizer.from_pretrained(model_name)
#     model = T5ForConditionalGeneration.from_pretrained(model_name)

#     # Tokenize input text
#     inputs = tokenizer.encode("Please provide service details in 2 lines from Terralogic software solutions for" + input_text + "as response with warmful respect without mentioning user name." + input_text, return_tensors="pt", max_length=512, truncation=True)

#     # Generate summary
#     summary_ids = model.generate(inputs, max_length=150, length_penalty=2.0, num_beams=4, early_stopping=True)
#     summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

#     return summary

# def summarize(requirements, num_sentences=3):
#     sentences = requirements.split(". ")  # Split text into sentences
#     sentences = [sentence.strip() for sentence in sentences]  # Remove leading/trailing spaces
#     ranked_sentences = sorted(sentences, key=len, reverse=True)[:num_sentences]  # Prioritize longer sentences
#     return " ".join(ranked_sentences)


class SendProjectEnquiryEmail(Resource):
    def post(self):
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        company = request.form.get('company')
        userRequirements = request.form.get('userRequirements')
        userFile = request.files['userFile']
        reactTime = request.form.get('reactTime')
        if not name or not email or not mobile or not company or not userRequirements:
            return emptyDataResponse()
        else:
            if reactTime == '':
                reactTime = "Not applicable"
            if userFile.filename == '':
                userFile = "None"
                fileName = "None"
            filePath = "None"
            if userFile != "None":
                userFile.save('D:\\chatGPT\\POC_GPT\\POC_GPT\\src\server\\TLChatBot\\uploadedFiles\\' + userFile.filename)
                filePath = 'D:\\chatGPT\\POC_GPT\\POC_GPT\\src\\server\\TLChatBot\\uploadedFiles\\' + userFile.filename
                fileName = userFile.filename
            sendEmail = ProjectEnquiryMailing(userFile,filePath,fileName,name,mobile,email,company,reactTime,userRequirements)
            if (sendEmail == "Email sent Successfully."):
                # os.remove(uploadFilePath)
                # addData = customer.insert_one({"customerName":name,"customerEmail" :email,"customerMobile":mobile,"company":company,
                #                         "userRequirements":userRequirements,"filePath": filePath,"reactTime":reactTime})
                sendAcknowledgement = ProjectEnquiryAcknowledgement(name,email)
                response = {
                    "data" : "Email sent Successfully.",
                    "success" : True
                }
            else:
                response =  {
                    "data" : "Failed to send email.",
                    "success" : True
                }
        return response

def ProjectEnquiryAcknowledgement(userName,userEmail):
    recipient_emails = userEmail
    sender_email = 'pavanralla999@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = 'pavanralla999@gmail.com'
    smtp_password = 'unuqjazkevhjgyxd'
    # Attach the message to the email body
    #HTML part
    htmlContent="""<html>
    <head>
        <meta charset="UTF-8">
        <title>Email Content</title>
    </head>
    <body style="text-align: center; font-family: Arial, sans-serif;">
      <div>
        <table border="0" cellspacing="0" cellpadding="0" width="100%" style="min-width:600px;padding:80px 0 40px 0" bgcolor="#eaeef3">
      <tbody>
          <tr>
              <td>
                  <table border="0" cellspacing="0" cellpadding="0" width="720" align="center" style="width:720px">
                      <tbody>
                          <tr>
                              <td>
                                  <table border="0" width="640" align="center" style="width:640px">
                                      <tbody>
                                          <tr>
                                              <td width="100%" height="3px" align="center" bgcolor="#ff3397">&nbsp;</td>
                                          </tr>
                                          <tr>
                                              <td width="100%" bgcolor="#ffffff">
                                                  <table border="0" cellspacing="0" cellpadding="0" width="90%" align="center">
                                                      <tbody>
                                                          <tr>
                                                              <td align="center" style="width:70%;padding-top:30px"><img style="width:143px" src="https://ci3.googleusercontent.com/meips/ADKq_NY-sNfLNClfpP19WOzwA9AQ-_p3fADGQ4lqVaL3ePDrqc8736Lz2YlIJ40Fq26sDfdLwGTbTQ0ye_k_EeN0GtaRrenOu4nbCV1vzW4ZV1zEs19fHG7wDXBiSPgM=s0-d-e1-ft#https://terralogic.com/wp-content/themes/terralogic/img/brand-logo.png" alt="Terralogic logo" class="CToWUd" data-bit="iit"></td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center"><h1>Greetings!</h1></td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center">
                                                                  <p>Hello <span style="text-transform:capitalize"><b>"""+userName+""",</b></span> ,</p>
                                                                  <p>Thanks for getting in touch!
                                                                 We aim to respond to all enquiries within three business days; you will be hearing from us soon.  </p>
                                                              </td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center" style="width:100%;padding:30px 0 30px 0"><img src="https://ci3.googleusercontent.com/meips/ADKq_Na8bwJb3mXqNTHdIOgNsMuZq5c_H1mvX3CNbOJYFoXKpuKHRGi1N-cwj2XmBNiHxmws2eHWJNMissFQGYNIMwxGPne4BkhzNerjp-gTVlHFpAGO_j7hCh91ZrU=s0-d-e1-ft#https://terralogic.com/wp-content/themes/terralogic/img/thank-you.png" alt="placeholder image" class="CToWUd" data-bit="iit">
                                                                  <div dir="ltr" style="opacity:0.01">
                                                                      <div id="m_-2626702077964089885m_5564634163801599257:12z" role="button" aria-label="Download attachment ">
                                                                          <div></div>
                                                                      </div>
                                                                  </div>
                                                              </td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center">In the meantime, you can check us out on</td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center" style="width:100%;padding-bottom:10px">
                                                                  <table border="0" cellspacing="0" cellpadding="0" width="80%" align="center">
                                                                      <tbody>
                                                                          <tr>
                                                                              <td style="text-align:center"><a style="text-align:center;font-size:13px;color:#333333;line-height:29px;text-decoration:none;font-weight:bold" href="https://www.linkedin.com/company/terralogic/" title="Terralogic on Linkedin" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.linkedin.com/company/terralogic/&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw07z6GiJ96hwtOqLgqwhkBv">LinkedIn</a></td>
                                                                              <td style="text-align:center"><a style="text-align:center;font-size:13px;color:#333333;line-height:29px;text-decoration:none;font-weight:bold" href="https://twitter.com/Terralogic_" title="Terralogic on Twitter" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://twitter.com/Terralogic_&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw2636SSzGuCDYABxribWZa9">Twitter</a></td>

                                                                              <td style="text-align:center"><a style="text-align:center;font-size:13px;color:#333333;line-height:29px;text-decoration:none;font-weight:bold" href="https://www.facebook.com/TerralogicInc/" title="Terralogic on Facebook" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.facebook.com/TerralogicInc/&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw1gVOVkIm_XNwv8eFqL6XHR">Facebook</a></td>

                                                                               <td style="text-align:center"><a style="text-align:center;font-size:13px;color:#333333;line-height:29px;text-decoration:none;font-weight:bold" href="https://www.youtube.com/channel/UC_bktWm8wMCeEh7Ht3UhE-Q/videos" title="Terralogic on Youtube" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.youtube.com/channel/UC_bktWm8wMCeEh7Ht3UhE-Q/videos&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw0A7_r3QXkg0L-tNDxrZc7S">Youtube</a></td>
                                                                          </tr>
                                                                      </tbody>
                                                                  </table>
                                                              </td>
                                                          </tr>
                              <tr>
                                                               <td align="center">You can also look over our new success story collection or browse through our latest blog posts<a style="text-align:center;font-size:13px;color:#212529;line-height:29px;text-decoration:none;font-weight:bold" href="https://terralogic.com/blogs/" title="Terralogic Latest Blogs" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://terralogic.com/blogs/&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw1AVp3BB446HfGda_0HgTm-"><span style="color:#5d33ea;font-weight:bold"> here </span></a></td>
                                                         </tr>
                                                      </tbody>
                                                  </table>
                                              </td>
                                          </tr>
                                          <tr>
                                              <td align="center" style="width:90%;padding:28px 48px">&nbsp;</td>
                                          </tr>
                                      </tbody>
                                  </table>
                              </td>
                          </tr>
                      </tbody>
                  </table>
              </td>
          </tr>
      </tbody>
      </table><div class="yj6qo"></div><div class="adL">
    </body>
    </html>"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_emails
    msg['Subject'] = "Thank you for contacting Terralogic"
    msg.attach(MIMEText(htmlContent, 'html'))
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_emails, msg.as_string())
        response = "Email sent Successfully."
    except Exception as e:
        response = (f"Failed to send email. Error: {e}")
    return response

def ProjectEnquiryMailing(userFile,filePath,fileName,userName,userMobile,userEmail,userCompany,userReactTime,requirements):
    recipient_emails = ['pavanralla999@gmail.com','pavankalyanralla99@gmail.com']
    sender_email = 'pavanralla999@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = 'pavanralla999@gmail.com'
    smtp_password = 'unuqjazkevhjgyxd'
    # Attach the message to the email body
    #HTML part
    htmlContent ="""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">

    <table cellpadding="10" cellspacing="50" border="0" width="100%" style="max-width: 100%; margin: 0 auto; background-color: #ffffff; border: 1px solid #dddddd;">
        <tr>
        <td align="center">
            <img src="https://ci3.googleusercontent.com/meips/ADKq_NY-sNfLNClfpP19WOzwA9AQ-_p3fADGQ4lqVaL3ePDrqc8736Lz2YlIJ40Fq26sDfdLwGTbTQ0ye_k_EeN0GtaRrenOu4nbCV1vzW4ZV1zEs19fHG7wDXBiSPgM=s0-d-e1-ft#https://terralogic.com/wp-content/themes/terralogic/img/brand-logo.png" alt="Your Company Logo" style="max-width: 20%; height:20%; display: block;">
        </td>
        </tr>
        <tr>
        <td style="padding: 0px;">
            <p style="color: black;">First Name : <strong>"""+userName+"""</strong></p>
            <p style="color: black;">Phone : <strong>"""+userMobile+"""</strong></p>
            <p style="color: black;">Email : <strong>"""+userEmail+"""</strong></p>
            <p style="color: black;">Company Name : <strong>"""+userCompany+"""</strong></p>
            <p style="color: black;">Project Need to Start : <strong>"""+userReactTime+"""</strong></p>
            <p style="color: black;">Message : <strong>"""+requirements+"""</strong></p>
        </td>
        </tr>
    </table>
    </body>
    </html>"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_emails)
    msg['Subject'] = "Project Enquiry from "+userName

    msg.attach(MIMEText(htmlContent, 'html'))
    try:
        if userFile != "None":
            with open(filePath, 'rb') as attachment:
                part = MIMEApplication(attachment.read(), Name=fileName)
                part['Content-Disposition'] = f'attachment; filename="{fileName}"'
                msg.attach(part)
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_emails, msg.as_string())
        response = "Email sent Successfully."
    except Exception as e:
        response = (f"Failed to send email. Error: {e}")
    return response

class SendCareerEnquiryEmail(Resource):
    def post(self):
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        location = request.form.get('location')
        jobLookingFor = request.form.get('jobLookingFor')
        userFile = request.files['userFile']
        if not name or not email or not mobile or not location or not jobLookingFor:
            return emptyDataResponse()
        else:
            if userFile.filename == '':
                userFile = "None"
                fileName = "None"
            filePath = "None"
            if userFile != "None":
                userFile.save('D:\\chatGPT\\POC_GPT\\POC_GPT\\src\server\\TLChatBot\\uploadedFiles\\' + userFile.filename)
                filePath = 'D:\\chatGPT\\POC_GPT\\POC_GPT\\src\\server\\TLChatBot\\uploadedFiles\\' + userFile.filename
                fileName = userFile.filename
            sendEmail = CareerEnquiryMailing(userFile,filePath,fileName,name,mobile,email,location,jobLookingFor)
            if (sendEmail == "Email sent Successfully."):
                sendAcknowlegment = CareerEnquiryAcknowledgement(name,email)
                response = {
                    "data" : "Email sent Successfully.",
                    "success" : True
                }
            else:
                response = {
                    "data" : "Failed to send email.",
                    "success" : True
                }
        return response

def CareerEnquiryMailing(userFile,filePath,fileName,userName,userMobile,userEmail,location,jobLookingFor):
    recipient_emails = 'pavanralla999@gmail.com'
    sender_email = 'pavanralla999@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = 'pavanralla999@gmail.com'
    smtp_password = 'unuqjazkevhjgyxd'
    # Attach the message to the email body
    #HTML part
    htmlContent ="""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">

    <table cellpadding="10" cellspacing="50" border="0" width="100%" style="max-width: 100%; margin: 0 auto; background-color: #ffffff; border: 1px solid #dddddd;">
        <tr>
        <td align="center">
            <img src="https://ci3.googleusercontent.com/meips/ADKq_NY-sNfLNClfpP19WOzwA9AQ-_p3fADGQ4lqVaL3ePDrqc8736Lz2YlIJ40Fq26sDfdLwGTbTQ0ye_k_EeN0GtaRrenOu4nbCV1vzW4ZV1zEs19fHG7wDXBiSPgM=s0-d-e1-ft#https://terralogic.com/wp-content/themes/terralogic/img/brand-logo.png" alt="Your Company Logo" style="max-width: 20%; height:20%; display: block;">
        </td>
        </tr>
        <tr>
        <td style="padding: 0px;">
            <p style="color: black;">First Name : <strong>"""+userName+"""</strong></p>
            <p style="color: black;">Phone : <strong>"""+userMobile+"""</strong></p>
            <p style="color: black;">Email : <strong>"""+userEmail+"""</strong></p>
            <p style="color: black;">Job Location : <strong>"""+location+"""</strong></p>
            <p style="color: black;">JobLookingFor : <strong>"""+jobLookingFor+"""</strong></p>
        </td>
        </tr>
    </table>
    </body>
    </html>"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_emails
    msg['Subject'] = "Career Enquiry for "
    msg.attach(MIMEText(htmlContent, 'html'))
    try:
        if userFile != "None":
            with open(filePath, 'rb') as attachment:
                part = MIMEApplication(attachment.read(), Name=fileName)
                part['Content-Disposition'] = f'attachment; filename="{fileName}"'
                msg.attach(part)
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_emails, msg.as_string())
        response = "Email sent Successfully."
    except Exception as e:
        response = (f"Failed to send email. Error: {e}")
    return response

def CareerEnquiryAcknowledgement(userName,userEmail):
    recipient_emails = userEmail
    sender_email = 'pavanralla999@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = 'pavanralla999@gmail.com'
    smtp_password = 'unuqjazkevhjgyxd'
    # Attach the message to the email body
    #HTML part
    htmlContent="""<html>
    <head>
        <meta charset="UTF-8">
        <title>Email Content</title>
    </head>
    <body style="text-align: center; font-family: Arial, sans-serif;">
      <div>
        <table border="0" cellspacing="0" cellpadding="0" width="100%" style="min-width:600px;padding:80px 0 40px 0" bgcolor="#eaeef3">
      <tbody>
          <tr>
              <td>
                  <table border="0" cellspacing="0" cellpadding="0" width="720" align="center" style="width:720px">
                      <tbody>
                          <tr>
                              <td>
                                  <table border="0" width="640" align="center" style="width:640px">
                                      <tbody>
                                          <tr>
                                              <td width="100%" height="3px" align="center" bgcolor="#ff3397">&nbsp;</td>
                                          </tr>
                                          <tr>
                                              <td width="100%" bgcolor="#ffffff">
                                                  <table border="0" cellspacing="0" cellpadding="0" width="90%" align="center">
                                                      <tbody>
                                                          <tr>
                                                              <td align="center" style="width:70%;padding-top:30px"><img style="width:143px" src="https://ci3.googleusercontent.com/meips/ADKq_NY-sNfLNClfpP19WOzwA9AQ-_p3fADGQ4lqVaL3ePDrqc8736Lz2YlIJ40Fq26sDfdLwGTbTQ0ye_k_EeN0GtaRrenOu4nbCV1vzW4ZV1zEs19fHG7wDXBiSPgM=s0-d-e1-ft#https://terralogic.com/wp-content/themes/terralogic/img/brand-logo.png" alt="Terralogic logo" class="CToWUd" data-bit="iit"></td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center"><h1>Thank you!</h1></td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center">
                                                                  <p>Hello <span style="text-transform:capitalize"><b>"""+userName+""",</b></span> ,</p>
                                                                  <p>Thank you for showing interest in being a part of the Terralogic family. We will get back to you soon..  </p>
                                                              </td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center" style="width:100%;padding:30px 0 30px 0"><img src="https://ci3.googleusercontent.com/meips/ADKq_Na8bwJb3mXqNTHdIOgNsMuZq5c_H1mvX3CNbOJYFoXKpuKHRGi1N-cwj2XmBNiHxmws2eHWJNMissFQGYNIMwxGPne4BkhzNerjp-gTVlHFpAGO_j7hCh91ZrU=s0-d-e1-ft#https://terralogic.com/wp-content/themes/terralogic/img/thank-you.png" alt="placeholder image" class="CToWUd" data-bit="iit">
                                                                  <div dir="ltr" style="opacity:0.01">
                                                                      <div id="m_-2626702077964089885m_5564634163801599257:12z" role="button" aria-label="Download attachment ">
                                                                          <div></div>
                                                                      </div>
                                                                  </div>
                                                              </td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center">Do check us out on</td>
                                                          </tr>
                                                          <tr>
                                                              <td align="center" style="width:100%;padding-bottom:10px">
                                                                  <table border="0" cellspacing="0" cellpadding="0" width="80%" align="center">
                                                                      <tbody>
                                                                          <tr>
                                                                              <td style="text-align:center"><a style="text-align:center;font-size:13px;color:#333333;line-height:29px;text-decoration:none;font-weight:bold" href="https://www.linkedin.com/company/terralogic/" title="Terralogic on Linkedin" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.linkedin.com/company/terralogic/&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw07z6GiJ96hwtOqLgqwhkBv">LinkedIn</a></td>
                                                                              <td style="text-align:center"><a style="text-align:center;font-size:13px;color:#333333;line-height:29px;text-decoration:none;font-weight:bold" href="https://twitter.com/Terralogic_" title="Terralogic on Twitter" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://twitter.com/Terralogic_&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw2636SSzGuCDYABxribWZa9">Twitter</a></td>

                                                                              <td style="text-align:center"><a style="text-align:center;font-size:13px;color:#333333;line-height:29px;text-decoration:none;font-weight:bold" href="https://www.facebook.com/TerralogicInc/" title="Terralogic on Facebook" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.facebook.com/TerralogicInc/&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw1gVOVkIm_XNwv8eFqL6XHR">Facebook</a></td>

                                                                               <td style="text-align:center"><a style="text-align:center;font-size:13px;color:#333333;line-height:29px;text-decoration:none;font-weight:bold" href="https://www.youtube.com/channel/UC_bktWm8wMCeEh7Ht3UhE-Q/videos" title="Terralogic on Youtube" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://www.youtube.com/channel/UC_bktWm8wMCeEh7Ht3UhE-Q/videos&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw0A7_r3QXkg0L-tNDxrZc7S">Youtube</a></td>
                                                                          </tr>
                                                                      </tbody>
                                                                  </table>
                                                              </td>
                                                          </tr>
                              <tr>
                                                               <td align="center">Because we believe knowlege is for sharing. visit our blogs posts<a style="text-align:center;font-size:13px;color:#212529;line-height:29px;text-decoration:none;font-weight:bold" href="https://terralogic.com/blogs/" title="Terralogic Latest Blogs" target="_blank" data-saferedirecturl="https://www.google.com/url?q=https://terralogic.com/blogs/&amp;source=gmail&amp;ust=1709021385543000&amp;usg=AOvVaw1AVp3BB446HfGda_0HgTm-"><span style="color:#5d33ea;font-weight:bold"> here </span></a></td>
                                                         </tr>
                                                      </tbody>
                                                  </table>
                                              </td>
                                          </tr>
                                          <tr>
                                              <td align="center" style="width:90%;padding:28px 48px">&nbsp;</td>
                                          </tr>
                                      </tbody>
                                  </table>
                              </td>
                          </tr>
                      </tbody>
                  </table>
              </td>
          </tr>
      </tbody>
      </table><div class="yj6qo"></div><div class="adL">
    </body>
    </html>"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_emails
    msg['Subject'] = "Thanks for Reaching Out, We will get back to you soon!"
    msg.attach(MIMEText(htmlContent, 'html'))
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_emails, msg.as_string())
        response = "Email sent Successfully."
    except Exception as e:
        response = (f"Failed to send email. Error: {e}")
    return response


class SendOthersEmail(Resource):
    def post(self):
        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        company = request.form.get('company')
        userRequirements = request.form.get('userRequirements')
        userFile = request.files['userFile']
        if not name or not email or not mobile or not company or not userRequirements:
            return emptyDataResponse()
        else:
            if userFile.filename == '':
                userFile = "None"
                fileName = "None"
            filePath = "None"
            if userFile != "None":
                userFile.save('D:\\chatGPT\\POC_GPT\\POC_GPT\\src\server\\TLChatBot\\uploadedFiles\\' + userFile.filename)
                filePath = 'D:\\chatGPT\\POC_GPT\\POC_GPT\\src\\server\\TLChatBot\\uploadedFiles\\' + userFile.filename
                fileName = userFile.filename
            sendEmail = OthersMailing(userFile,filePath,fileName,name,mobile,email,company,userRequirements)
            if (sendEmail == "Email sent Successfully."):
                response = {
                    "data" : "Email sent Successfully.",
                    "success" : True
                }
            else:
                response = {
                    "data" : "Failed to send email.",
                    "success" : True
                }
        return response

def OthersMailing(userFile,filePath,fileName,userName,userMobile,userEmail,userCompany,requirements):
    recipient_emails = 'pavanralla999@gmail.com'
    sender_email = 'pavanralla999@gmail.com'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 465
    smtp_username = 'pavanralla999@gmail.com'
    smtp_password = 'unuqjazkevhjgyxd'
    # Attach the message to the email body
    #HTML part
    htmlContent ="""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">

    <table cellpadding="10" cellspacing="50" border="0" width="100%" style="max-width: 100%; margin: 0 auto; background-color: #ffffff; border: 1px solid #dddddd;">
        <tr>
        <td align="center">
            <img src="https://ci3.googleusercontent.com/meips/ADKq_NY-sNfLNClfpP19WOzwA9AQ-_p3fADGQ4lqVaL3ePDrqc8736Lz2YlIJ40Fq26sDfdLwGTbTQ0ye_k_EeN0GtaRrenOu4nbCV1vzW4ZV1zEs19fHG7wDXBiSPgM=s0-d-e1-ft#https://terralogic.com/wp-content/themes/terralogic/img/brand-logo.png" alt="Your Company Logo" style="max-width: 20%; height:20%; display: block;">
        </td>
        </tr>
        <tr>
        <td style="padding: 0px;">
            <p style="color: black;">First Name : <strong>"""+userName+"""</strong></p>
            <p style="color: black;">Phone : <strong>"""+userMobile+"""</strong></p>
            <p style="color: black;">Email : <strong>"""+userEmail+"""</strong></p>
            <p style="color: black;">Company Name : <strong>"""+userCompany+"""</strong></p>
            <p style="color: black;">Message : <strong>"""+requirements+"""</strong></p>
        </td>
        </tr>
    </table>
    </body>
    </html>"""
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_emails
    msg['Subject'] = "Business Enquiry from "+userName
    msg.attach(MIMEText(htmlContent, 'html'))
    try:
        if userFile != "None":
            with open(filePath, 'rb') as attachment:
                part = MIMEApplication(attachment.read(), Name=fileName)
                part['Content-Disposition'] = f'attachment; filename="{fileName}"'
                msg.attach(part)
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_username, smtp_password)
            server.sendmail(smtp_username, recipient_emails, msg.as_string())
        response = "Email sent Successfully."
    except Exception as e:
        response = (f"Failed to send email. Error: {e}")
    return response
