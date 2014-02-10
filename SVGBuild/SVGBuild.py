# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
import subprocess
import shutil
import time
import sys
import re

import interpolations
import vectors
from vectors import *

from PyQt4 import QtCore
from SVG import SVG
from Camera import Camera
from Settings import Settings
from lxml import etree

class SVGBuild(QtCore.QObject):    
    finished = QtCore.pyqtSignal()
    canceled = QtCore.pyqtSignal()
    printText = QtCore.pyqtSignal(QtCore.QString)
    
    svg = SVG()
    options = { 'folder': 'movie',
            'name': 'movie',
            'temp': 'temp.svg',
            'from': 0,
            'until': 99999,
            'image': False,
            'path': False,
            'fullpath': False,
            'top': False,
            'page': False,
            'combine': False,
            'camera': False,
            'line' : '#000000',
            'frame' : '#FF0000',
            'text': False,
            'backward': False,
            'width': 640,
            'height': 480,
            'dally': 4,
            'dolly': 50,
            'hold': 100,
            'background': '#FFFFFF',
            'zoom': 6.,
            'xx': False
            }
            
    isRunning = False
    
    def __init__(self):
        super(SVGBuild, self).__init__()
        self.camera = Camera(self.options)
        
    def setFilename(self, filename):
        self.filename = filename
        
    def setIsRunning(self,  isRunning):
        self.isRunning = isRunning
        
        if not isRunning:
            self.camera.setIsRunning(isRunning)
            self.canceled.emit()
        
    def getOptions(self):
        return self.options
        
    def setSingleOption(self, key,  value):
        self.options[key] = value
        
    def getSingleOption(self, key):
        return self.options[key]
        
    def getPathOption(self):
        return self.getSingleOption('path')
        
    def getFullPathOption(self):
        return self.getSingleOption('fullpath')
        
    def getCameraOption(self):
        return self.getSingleOption('camera')
        
    def getPageOption(self):
        return self.getSingleOption('page')
    
    def startBuildUp(self):
        if self.options['width'] < 1 or self.options['height'] < 1:
            print 'Invalid output pixel --height or --width specified.'
        if zero(self.options['zoom']) or self.options['zoom'] < 0:
            print 'Zoom limiting value is invalid; must be positive.'
        if self.options['xx']:
            self.options['from'] = self.options['until'] = -1
        if self.options['fullpath']:
            self.options['path'] = True

        # overall preparations
        overall = time.time()

        folder_name = [ self.options['folder'], self.options['name'] ]
        
        if not QtCore.QFile.exists(self.filename):
               print 'SVG files were not found.'
        else:
            fileInfo = QtCore.QFileInfo(self.filename);
            
            if folder_name[0] == 'movie':
                self.options['folder'] = fileInfo.baseName()
            if folder_name[1] == 'movie':
                self.options['name'] = fileInfo.baseName()
            if self.options['page']:
                self.options['folder'] += '_page'
            if self.options['backward']:
                self.options['folder'] += '_backward'

            if not os.path.exists(self.options['folder']):
                os.mkdir(self.options['folder'])
                
            start = time.time()
            self.printText.emit('Starting buildup of %s...' % self.filename)
            
            try:
                self.svg = SVG()
                elementCount = self.svg.read(str(self.filename))
            except Exception as e:
                print 'error'
                self.finished.emit()
                return
            
            if self.options['fullpath']:
                defs_element = self.svg.root.find('{http://www.w3.org/2000/svg}defs')
                markers = defs_element.findall('{http://www.w3.org/2000/svg}marker')
                
                if len(markers) == 0:
                    self.addMarker(defs_element, self.options['marker'])
                else:
                   self.marker = '%s' % markers[0].attrib['id']
            
            self.printText.emit('Surveyed %d elements.' % elementCount)
            
            self.camera = Camera(self.options)
            self.camera.printText.connect(self.printText)
            
            if self.camera.survey(self.svg):
                #self.printText.emit('ok')
                self.build(self.svg, self.camera, self.svg.root, self.options)
                
                if self.isRunning:
                    self.printText.emit('Finishing...')
                    self.options['camera'] = False
                    self.camera.shoot(self.svg)
                    self.camera.hold(self.options['hold'])
                    self.camera.cleanup()
                else:
                    self.printText.emit('Canceled...')
            
            finish = time.time()
            hours = int((finish - start) / 60) / 60
            minutes = int((finish - start) / 60) % 60
            folder = self.options['folder']
            self.printText.emit('Finished %s to %s in %dh:%02dm.' % (self.filename, folder, hours, minutes))
            
        self.finished.emit()
        
    def build(self, svg, camera, entity, options):
        '''Recursively build up the given entity, by removing all its children
        and adding them back in one at a time, and shooting the progress with
        the given camera.
        '''
        
        if not self.isRunning: return

        id = entity.attrib['id']
        name = id
        label = 'http://www.inkscape.org/namespaces/inkscape}label'
        if label in entity.attrib:
            name = entity.attrib[label]
        #print '%05d - Building up <%s id="%s"> (%s)...' % (camera.time, entity.tag, id, name)
        self.printText.emit('%05d - Building up <%s id="%s"> (%s)...' % (camera.time, entity.tag, id, name))

        nobuild = set([ '{http://www.w3.org/2000/svg}defs',
                        '{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}namedview',
                        '{http://www.w3.org/2000/svg}metadata',
                        ])

        nochild = set([ '{http://www.w3.org/2000/svg}text',
                        ])

        backable = set([ '{http://www.w3.org/2000/svg}svg',
                         '{http://www.w3.org/2000/svg}g',
                        ])

        ripped = [ ]
        for child in entity.iterchildren():
            if child.tag in nobuild: continue
            if not child.attrib['id'] in camera.layout: continue
            if 'style' in child.attrib:
                if 'display:none' in child.attrib['style']:
                    continue
            ripped.append(child)
        for child in ripped:
            entity.remove(child)

        backward = False    
        
        '''build from the lowest object'''
        if entity.tag in backable and self.options['backward']:
            backward = True
        
        '''build from the top object'''
        if backward:
            self.printText.emit(' (Building children of entity %s backwards.)' % id)
            #print ' (Building children of entity %s backwards.)' % id
            ripped.reverse()

        for child in ripped:
            if not self.isRunning: return
            self.printText.emit(' Adding child <%s id="%s">...' % (child.tag, child.attrib['id']))
            #print ' Adding child <%s id="%s">...' % (child.tag, child.attrib['id'])
            
            if self.options['page']:
                if self.options['camera']:
                    camera.pan(svg, child.attrib['id'], margin=1.2)

                camera.shoot(svg)
            else:
                camera.pan(svg, child.attrib['id'], margin=1.2)

            if child.getchildren() and not child.tag in nochild:
                if backward:
                    entity.insert(0, child)
                else:
                    entity.append(child)

                self.build(svg, camera, child, options)
            else:
                if self.options['top']:
                    svg.root.append(child)
                else:
                    if backward:
                        entity.insert(0, child)
                    else:
                        entity.append(child)

                if self.options['path'] and re.search(r"\}path$", child.tag):
                    self.build_path(svg, camera, child, options)
                elif self.options['image'] and re.search(r"\}image$", child.tag):
                    self.build_image(svg, camera, child, options)
                elif self.options['text'] and re.search(r"\}text$", child.tag):
                    self.build_text(svg, camera, child, options)
                else:
                    camera.shoot(svg)

                if self.options['top']:
                    svg.root.remove(child)
                    if backward:
                        entity.insert(0, child)
                    else:
                        entity.append(child)

            camera.shoot(svg)
            camera.hold(self.options['dally'] - 1)

        camera.pan(svg, id)
        
    def build_image(self, svg, camera, entity, options):
        '''Special progressive drawing of an image element.
        The image will be included a few scanlines at a time until whole.'''
        
        if not self.isRunning: return
        
        href = '{http://www.w3.org/1999/xlink}href'
        if not href in entity.attrib: return
        if not os.path.exists(Settings.identify):
            print 'ImageMagick "identify" tool not found; skipping.'
            return
        if not os.path.exists(Settings.convert):
            print 'ImageMagick "convert" tool not found; skipping.'
            return
        img = entity.attrib[href]
        if not os.path.exists(img):
            print 'Image file not found locally:', img
            return
        # figure out original image's pixel size
        results = Utils.qx('%s %s' % (str(Settings.identify), img))
        m = re.search(r'(\d+)x(\d+)', results)
        if not m:
            print 'ImageMagick could not identify size of image; skipping.'
            return
        size = [ int(m.group(1)), int(m.group(2)) ]
        # for a handful of frames, replace image with a truncated temporary image
        tmp = self.options['folder'] + '/temp.png'
        frames = int(self.options['dally']) * 4
        for frame in range(frames):
            height = interpolations.linear(0, frames, frame, 1, size[1])
            command = ' '.join( [ str(Settings.convert),
                                  '-type TrueColorMatte',
                                  '-channel alpha',
                                  img,
                                  '-background "#00000000"',
                                  '-crop %dx%d+0+0' % (size[0], height),
                                  '-extent %dx%d' % (size[0], size[1]),
                                  tmp ] )
            results = Utils.qx(command)
            if os.path.exists(tmp):
                entity.attrib[href] = tmp
                camera.shoot(svg)
                os.unlink(tmp)
        # replace the original image reference
        entity.attrib[href] = img
        camera.shoot(svg)

    def build_path(self, svg, camera, entity, options):
        '''Special progressive drawing of a path element.
        The path will be included one bezier element at a time until whole.'''
        if not 'd' in entity.attrib: return
        # replace style with our own style
        style = ''
        if 'style' in entity.attrib:
            style = entity.attrib['style']
        width = (camera.area[3]-camera.area[1]) / float(camera.height)
        if self.options['page']:
            page_width = float(svg.root.attrib['width'])
            page_height = float(svg.root.attrib['height'])
            if page_width > page_height:
                width = page_width / page_height
            else:
                width = page_height / page_width
        hl = [
        'opacity:1', 'overflow:visible',
        'fill:none',
        'fill-opacity:0.',
        'fill-rule:nonzero',
        'stroke:%s' % self.options['line'],
        'stroke-width:%f' % width,
        'stroke-linecap:round', 'stroke-linejoin:round',
        'marker:none',
        'marker-start:none',
        'marker-mid:none',
        #~ 'marker-end:none',
        'stroke-miterlimit:4', 'stroke-dasharray:none',
        'stroke-dashoffset:0', 'stroke-opacity:1',
        'visibility:visible', 'display:inline',
        'enable-background:accumulate' 
        ]

        if self.options['fullpath']:
            hl.append('marker-end:url(#%s)' % self.marker)
            #~ hl.append('marker-start:url(#Arrow1Lstart)')
            #~ hl[12] = 'marker-end:url(#SquareL)'
        else:
            hl.append('marker-end:none')
            #~ hl.append('marker-start:none')

        hairline = ';'.join(hl)
        
        #~ print hairline

        entity.attrib['style'] = hairline
        # scan the control points
        points = entity.attrib['d'].split(' ')
        built = [ ]
        # each control point is a letter, followed by some floating-point pairs
        while points:
            if not self.isRunning: return
            built.append( points.pop(0) )
            if not self.options['fullpath']:
                while points and not re.match(r'^[a-zA-Z]$', points[0]):
                    built.append( points.pop(0) )
            
            # add the point to our path
            entity.attrib['d'] = ' '.join(built)
            camera.shoot(svg)
        # put the original style back
        entity.attrib['style'] = style
        camera.shoot(svg)

        camera.shoot(svg)

    def build_text(self, svg, camera, entity, options):
        '''Special progressive drawing of a text or tspan contents.
        The text will appear one letter at a time until whole.'''
        text = entity.text
        entity.text = ''
        # if we have children, recurse to build their .text now
        if entity.getchildren():
            children = [ ]
            for child in entity.iterchildren():
                if child.text:
                    children.append(child)
            for child in children:
                entity.remove(child)
            for child in children:
                entity.append(child)
                build_text(svg, camera, child, options)
        # come back to build our own direct text
        if not text: return
        for l in range(1, len(text)):
            if not self.isRunning: return
            entity.text = text[:l]
            camera.shoot(svg)
        entity.text = text
        camera.shoot(svg)
        
    def addMarker(self,  element, name='diamond'):
        print name
        if name == 'diamond':
            marker_element = etree.SubElement(element, 'marker', id = 'EmptyDiamondL')
            marker_element.set('{http://www.inkscape.org/namespaces/inkscape}stockid', 'EmptyDiamondL')
            marker_element.set('refY', '0.0')
            marker_element.set('style', 'overflow:visible')
            marker_element.set('refX', '0.0')
            marker_element.set('orient', 'auto')
            marker_element.set('id', 'EmptyDiamondL')

            marker_path = etree.SubElement(marker_element, '{http://www.w3.org/2000/svg}path', id ='mark0001')
            marker_path.set('d', "M 0,-7.0710768 L -7.0710894,0 L 0,7.0710589 L 7.0710462,0 L 0,-7.0710768 z ")
            marker_path.set('style', "fill-rule:evenodd;fill:#FFFFFF;stroke:#000000;stroke-width:1.0pt")
            marker_path.set('transform', "scale(0.8)")

            self.marker = '%s' % marker_element.attrib['id']
        
        elif name == 'scissor':
            marker_element = etree.SubElement(element, 'marker', id = 'Scissors')
            marker_element.set('{http://www.inkscape.org/namespaces/inkscape}stockid', 'Scissors')
            marker_element.set('refY', '0.0')
            marker_element.set('style', 'overflow:visible')
            marker_element.set('refX', '0.0')
            marker_element.set('orient', 'auto')
            marker_element.set('id', 'Scissors')

            marker_path = etree.SubElement(marker_element, '{http://www.w3.org/2000/svg}path', id ='schere')
            marker_path.set('d', "M 9.0898857,-3.6061018 C 8.1198849,-4.7769976 6.3697607,-4.7358294 5.0623558,-4.2327734 L -3.1500488,-1.1548705 C -5.5383421,-2.4615840 -7.8983361,-2.0874077 -7.8983361,-2.7236578 C -7.8983361,-3.2209742 -7.4416699,-3.1119800 -7.5100293,-4.4068519 C -7.5756648,-5.6501286 -8.8736064,-6.5699315 -10.100428,-6.4884954 C -11.327699,-6.4958500 -12.599867,-5.5553341 -12.610769,-4.2584343 C -12.702194,-2.9520479 -11.603560,-1.7387447 -10.304005,-1.6532027 C -8.7816644,-1.4265411 -6.0857470,-2.3487593 -4.8210600,-0.082342643 C -5.7633447,1.6559151 -7.4350844,1.6607341 -8.9465707,1.5737277 C -10.201445,1.5014928 -11.708664,1.8611256 -12.307219,3.0945882 C -12.885586,4.2766744 -12.318421,5.9591904 -10.990470,6.3210002 C -9.6502788,6.8128279 -7.8098011,6.1912892 -7.4910978,4.6502760 C -7.2454393,3.4624530 -8.0864637,2.9043186 -7.7636052,2.4731223 C -7.5199917,2.1477623 -5.9728246,2.3362771 -3.2164999,1.0982979 L 5.6763468,4.2330688 C 6.8000164,4.5467672 8.1730685,4.5362646 9.1684433,3.4313614 L -0.051640930,-0.053722219 L 9.0898857,-3.6061018 z M -9.2179159,-5.5066058 C -7.9233569,-4.7838060 -8.0290767,-2.8230356 -9.3743431,-2.4433169 C -10.590861,-2.0196559 -12.145370,-3.2022863 -11.757521,-4.5207817 C -11.530373,-5.6026336 -10.104134,-6.0014137 -9.2179159,-5.5066058 z M -9.1616516,2.5107591 C -7.8108215,3.0096239 -8.0402087,5.2951947 -9.4138723,5.6023681 C -10.324932,5.9187072 -11.627422,5.4635705 -11.719569,4.3902287 C -11.897178,3.0851737 -10.363484,1.9060805 -9.1616516,2.5107591 z ")
            marker_path.set('style', "fill:#000000;")
            #marker_path.set('transform', "scale(0.8)")

            self.marker = '%s' % marker_element.attrib['id']
            
        elif name == 'triangle':
            marker_element = etree.SubElement(element, 'marker', id = 'EmptyTriangleOutL')
            marker_element.set('{http://www.inkscape.org/namespaces/inkscape}stockid', 'EmptyTriangleOutL')
            marker_element.set('refY', '0.0')
            marker_element.set('style', 'overflow:visible')
            marker_element.set('refX', '0.0')
            marker_element.set('orient', 'auto')
            marker_element.set('id', 'EmptyTriangleOutL')

            marker_path = etree.SubElement(marker_element, '{http://www.w3.org/2000/svg}path', id ='mark0002')
            marker_path.set('d', "M 5.77,0.0 L -2.88,5.0 L -2.88,-5.0 L 5.77,0.0 z ")
            marker_path.set('style', "fill-rule:evenodd;fill:#FFFFFF;stroke:#000000;stroke-width:1.0pt")
            marker_path.set('transform', "scale(0.8) translate(-6,0)")

            self.marker = '%s' % marker_element.attrib['id']
            
