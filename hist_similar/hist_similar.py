# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw


def make_regalur_image(img, size=(256, 256)):
	return img.resize(size).convert('RGB')


def split_image(img, part_size=(64, 64)):  # 把图像分为4x4 块，每块的分辨率为64x64
	w, h = img.size
	pw, ph = part_size
	assert w % pw == h % ph == 0
	return [img.crop((i, j, i + pw, j + ph)).copy()
	        for i in range(0, w, pw)
	        for j in range(0, h, ph)]


def hist_similar(lh, rh):
	# 断言：声明以下表达式的布尔值必须为真，
	# 若表达式为假则会发生异常并返回异常参数
	assert len(lh) == len(rh), "error"
	return sum(1 - (0 if l == r else float(abs(l - r)) / max(l, r)) for l, r in zip(lh, rh)) / len(lh)


def calc_similar(li, ri):
	# return hist_similar(li.histogram(), ri.histogram())
	return sum(hist_similar(l.histogram(), r.histogram()) for l, r in zip(split_image(li), split_image(ri))) / 16.0


def calc_similar_by_path(lf, rf):
	li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
	return calc_similar(li, ri)


def draw_line(img, path):
	draw = ImageDraw.Draw(img)
	for i in range(0, 256, 64):
		draw.line((0, i, 256, i), fill='#ff0000')
		draw.line((i, 0, i, 256), fill='#ff0000')
	img.save(path + '-lines.png')


def make_doc_data(lf, rf, index):
	li, ri = make_regalur_image(Image.open(lf)), make_regalur_image(Image.open(rf))
	li.save(lf + '_regalur.png')
	ri.save(rf + '_regalur.png')
	fd = open('stat%d.csv' % (index), 'w')
	fd.write('\n'.join(l + ',' + r for l, r in zip(map(str, li.histogram()), map(str, ri.histogram()))))
	# print >>fd, '\n'
	# fd.write(','.join(map(str, ri.histogram())))
	fd.close()
	draw_line(li.convert('RGB'), lf)
	draw_line(ri.convert('RGB'), rf)


if __name__ == '__main__':
	for i in range(1, 7):
		print('test_case_%d: %.3f%%' % (i,
		                                calc_similar_by_path('test/TEST%d/%d.JPG' % (i, 1),
		                                                     'test/TEST%d/%d.JPG' % (i, 2)) * 100))
		make_doc_data('test/TEST%d/1.JPG' % (i), 'test/TEST%d/2.JPG' % (i), i)
