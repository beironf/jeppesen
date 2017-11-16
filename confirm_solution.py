
class ConfirmSolution(object):
	def __init__(self, forbidden_segs, forbidden_entry_segs, segments, points, entry_nodes, possible_destinations):
		self.forbidden_segs = forbidden_segs
		self.forbidden_entry_segs = forbidden_entry_segs
		self.segments = segments
		self.points = points
		self.entry_nodes = entry_nodes
		self.possible_destinations = possible_destinations
        self.possible_routes = []

	def isForbidden(self, seg, entry_seg):
		if entry_seg['from'] in self.entry_nodes:
			if seg in self.forbidden_segs[entry_seg['from']]:
				return True
		elif entry_seg['to'] in self.entry_nodes:
			if seg in self.forbidden_segs[entry_seg['to']]:
				return True
		else:
			if seg in self.forbidden_entry_segs:
				return True
			else:
				return False

	def getSegment(self, fr, to):
		seg = [seg for seg in self.segments if (seg['from']==fr and seg['to']==to)][0]
		return seg

	def find_path(self, seg, used_segs):
		node = seg['to']
		print(seg['from']+"       "+seg['to'])
		print('\n\n')
		for to in self.possible_destinations[node]:
			seg = self.getSegment(node, to)
			if self.isForbidden(seg, used_segs[0]):
				print('forbidden')
				if (to in self.entry_nodes or self.points[to]['area'][0]!='Z'):
					possible_routes.append(used_segs.append(seg))
			else:
				print('not forbidden')
				self.find_path(seg, used_segs.append(seg))


	def getPossibleRoutes(self):
		start_segs = []
        
		for seg in self.segments:
			fr = self.points[seg['from']]['area'][0]
			to = self.points[seg['to']]['area'][0]
			if (fr != 'Z' and to == 'Z'): # if seg is from another country to China
				start_segs.append(seg)

		for start_seg in start_segs:
			used_segs = [start_seg]
			self.find_path(start_seg, used_segs)

		return self.possible_routes

