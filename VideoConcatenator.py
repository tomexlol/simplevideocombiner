from moviepy.editor import *
import os
import math


class VideoCombinator:

	def __init__(self, vidList, vid_format=".mp4"):
		self.final_dur = 0
		self.final_dur_s = "00"
		self.final_dur_m = "00"
		self.final_vid = None
		self.vidList = vidList
		self.finalVidStarted = False
		self.it = 1
		self.current = 1
		self.total = len(self.vidList)
		
	def mergeVideos(self, settingsClipNumber, settingsClipName, settingsTimestamp, loggerino):
		for v in self.vidList:
			self.file_name = os.path.splitext(v)[0]	
			self.vid = VideoFileClip(v) #objeto del vid

			#print(f"Processing video {self.it} of {self.total}")
			
			if settingsClipNumber:	
				self.clipno = TextClip("Clip " + str(self.it), font="Amiri-Bold", fontsize=48, color="white").set_position((0,0)).set_duration(2) #genera 1 lnea de texto Clip X
				self.partialVid2 = CompositeVideoClip([self.vid, self.clipno])#sumar clipnumber a partialVid
				
			if settingsClipName:#case:name
				self.clipname = TextClip(os.path.splitext(os.path.basename(str(v)))[0], font="Amiri-Bold", fontsize=36, color="white").set_position((0,50)).set_duration(2) #genera subtitulo filename
				#lo de arriba seguro si o si falla jaja
				#also sumarlos!
				if settingsClipNumber:#case:name+number
					self.partialVid2 = CompositeVideoClip([self.partialVid2, self.clipname])#escribirle nombre al que tiene numerito
				else:
					self.partialVid2 = CompositeVideoClip([self.vid, self.clipname]) #escribirle nombre al raw
				
			if not settingsClipNumber and not settingsClipName: #simplifica las cosas, si no hay nada que agregar, pasamos de largo
				self.partialVid2 = self.vid
		
			
			if self.finalVidStarted:
				if settingsTimestamp:
					self.generateTimestamps(self.file_name)
				self.final_vid = concatenate_videoclips([self.final_vid, self.partialVid2])#si hay video final, sumar al video final	
			else:
				if settingsTimestamp:
					self.generateTimestamps(self.file_name)
				self.final_vid = self.partialVid2
				self.finalVidStarted = True
			
			if self.it == len(self.vidList):
				self.final_vid.write_videofile("SimplyCombinedVideo.mp4",logger=loggerino)
			else:
				self.it += 1
				continue		
				
				


						
	def generateTimestamps(self, fileName):
		actual_file_name = os.path.basename(fileName)
		with open("Timestamps.txt", "a") as text_file: #escribe el filename y la timestamp a un .txt
			text_file.write(f"{actual_file_name} ")
			text_file.write(str(self.final_dur_m) + ":" + str(self.final_dur_s) + "\n" )
		self.final_dur += self.partialVid2.duration #va contando los segundos totales
		self.formattedTime = divmod(self.final_dur, 60) #convierte a min, sec
		#actualiza mins, agregando un leading zero si tenemos 1 sola cifra
		if len(str(math.trunc(self.formattedTime[0]))) > 1:	
			self.final_dur_m = math.trunc(self.formattedTime[0])
		else:
			self.final_dur_m = str(math.trunc(self.formattedTime[0])).zfill(2)
		#actualiza secs, agregando un leading zero si tenemos 1 sola cifra
		if len(str(math.trunc(self.formattedTime[1]))) > 1:	
			self.final_dur_s = math.trunc(self.formattedTime[1])
		else:
			self.final_dur_s = str(math.trunc(self.formattedTime[1])).zfill(2)
