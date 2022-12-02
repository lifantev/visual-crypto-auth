import src.qr_coder as qr_coder
import src.visual_crypto as visual_crypto
import cv2 as cv
import numpy as np

def str2qr(string):
    qEncoder = qr_coder.qrEncoder()
    img = qEncoder.enc_str(string)
    return img

def qr2str(qr_path):
    qDecoder = qr_coder.qrDecoder()
    imgarr = cv.imread(qr_path)
    string = qDecoder.dec_str(qDecoder.process(imgarr))
    return string

def qr2vc(qr_img):
    cryptCoder = visual_crypto.cryptCoder()
    cryptCoder.get_msg(qr_img)
    img_sct = cryptCoder.get_sct()
    img_cph = cryptCoder.get_cph()
    return img_sct, img_cph

def vc2qr(img_sct, img_cph, qr_img):
    cryptCoder = visual_crypto.cryptCoder()
    cryptCoder.get_msg(qr_img)
    img_out = cryptCoder.get_out(img_sct, img_cph)
    return img_out
