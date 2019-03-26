#!/usr/bin/env python

import cherrypy
import xml.etree.ElementTree as ET
from agent.config import server_port
from agent.harvest import harvest
# from agent.transformer import transform


def get_request_host(request):
    host = request.headers.get('hostd')
    if not host:
        host = request.headers.get('host')
    return host


class AgentAPI(object):

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def harvest(self, **kwargs):
        results = harvest(kwargs)
        return results

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def transform(self, **kwargs):
        # results = transform(kwargs)
        return results

    @cherrypy.expose
    def default(self, *args, **kwargs):
        request = cherrypy.request
        host = get_request_host(request)
        url = "http://{}".format(host)
        cherrypy.log('root')

        root = ET.Element("html")
        body = ET.SubElement(root, "body")
        child = ET.SubElement(body, "h2")
        child.text = 'Welcome to the SAEON Metadata Harvesting Agent'
        api = ET.SubElement(body, "h3")
        api.text = 'API'
        ET.SubElement(api, "br")
        search = ET.SubElement(api, "a", {
            'href': '{}/harvest'.format(url)
        })
        search.text = 'Harvest'
        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = "Harvest metadata metadata files and upload them into a SAEON CKAN metadata server"

        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = 'Arguments:'

        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* transport: transport protocol to gather data. Currently only supports "FileSystem".'

        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* source_dir: the directory on the local file system where the text files reside'

        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* standard: the metadta type of the data files'

        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* upload_server_url: the end point into which the harvested records will be uploaded using either the give upload_method or jsonCreateMetadataAsJson'

        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* upload_user: the user to be used to add new records at the given upload_server_url'

        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* upload_password: the password to be used to add new records at the given upload_server_url'

        child = ET.SubElement(api, "br")
        child = ET.SubElement(api, "span", {
            'style': 'font-size: 12'})
        child.text = '* upload_method: the method to be used to add new records at the given upload_server_url'

        return ET.tostring(root)


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_port': server_port})
    cherrypy.config.update({'engine.autoreload.on': True})
    cherrypy.quickstart(AgentAPI(), '/')
