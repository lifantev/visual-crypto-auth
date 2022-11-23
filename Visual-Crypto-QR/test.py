import qr_coder
import visual_crypto
import cv2 as cv
from PIL import Image

def str2qr(string):
    qEncoder = qr_coder.qrEncoder()
    img = qEncoder.enc_str(string)
    img.save("./temp/msg.png")
    return img

def qr2str(qr_path):
    qDecoder = qr_coder.qrDecoder()
    imgarr = cv.imread(qr_path)
    string = qDecoder.dec_str(qDecoder.process(imgarr))
    return string

def qr2vc(qr_path):
    cryptCoder = visual_crypto.cryptCoder(path_dir='./temp/')
    # Get QR image
    img = Image.open("./temp/msg.png")
    cryptCoder.get_msg(img)
    # Generate secret and cipher image
    img_sct = cryptCoder.get_sct()
    img_cph = cryptCoder.get_cph()
    # Save or return
    img_sct.save("./temp/sct.png")
    img_cph.save("./temp/cph.png")
    return img_sct, img_cph

def vc2qr(img_sct, img_cph):
    cryptCoder = visual_crypto.cryptCoder(path_dir='./temp/')
    img = Image.open("./temp/msg.png")
    cryptCoder.get_msg(img)
    img_out = cryptCoder.get_out(img_sct, img_cph)
    img_out.save("./temp/out.png")
    return img_out

def test():
    str2qr("1234678")
    qr2vc("./temp/msg.png")
    vc2qr("./temp/sct.png", "./temp/cph.png")
    str = qr2str("./temp/out.png")
    print(str)


if __name__ == '__main__':
    test()