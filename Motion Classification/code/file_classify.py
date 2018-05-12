import re
import os
import shutil
columns_all = [
'root',
'lowerback',
'upperback',
'thorax',
'lowerneck',
'upperneck',
'head',
'rclavicle',
'rhumerus',
'rradius',
'rwrist',
'rhand',
'rfingers',
'rthumb',
'lclavicle',
'lhumerus',
'lradius',
'lwrist',
'lhand',
'lfingers',
'lthumb',
'rfemur',
'rtibia',
'rfoot',
'rtoes',
'lfemur',
'ltibia',
'lfoot',
'ltoes']

def main():
	src_path = 'data'
	if not os.path.exists(src_path):
		print('src dir not exists!')
		return

	dst_path = 'file_classified'
	if not os.path.exists(dst_path):
		os.mkdir(dst_path)

	walk_path = os.path.join(dst_path, 'walk')
	walk_path = os.path.join(os.path.abspath('.'), walk_path)
	if not os.path.exists(walk_path):
		os.mkdir(walk_path)

	other_path = os.path.join(dst_path, 'other')
	other_path = os.path.join(os.path.abspath('.'), other_path)
	if not os.path.exists(other_path):
		os.mkdir(other_path)

	fileClassify(src_path, walk_path, other_path)

def fileClassify(src, walk_path, other_path):
	if not os.path.isdir(src):
		print("not dir")
		return
	os.chdir(src)
	allFiles = os.listdir('.')
	for file in allFiles:
		print(file)
		if os.path.isdir(file):
			fileClassify(file, walk_path, other_path)
		elif file.split('.')[-1] != 'amc':
			continue
		else:
			if re.search('walk',file, re.I):
				shutil.copyfileobj(open(file,'r'), open(os.path.join(walk_path,file),'w'))
			else:
				shutil.copyfileobj(open(file,'r'), open(os.path.join(other_path,file),'w'))
	os.chdir('..')




def test():
	path = 'data/7 #walk'

	dst_path = 'file_classified'

	walk_path = os.path.join(dst_path, 'walk')
	walk_path = os.path.join(os.path.abspath('.'), walk_path)

	other_path = os.path.join(dst_path, 'other')
	other_path = os.path.join(os.path.abspath('.'), other_path)

	print(walk_path)
	print(other_path)

	# files = os.listdir('.')
	fileClassify(path, walk_path, other_path)
	# print(files)

if __name__=='__main__':
	# test()
	main()



