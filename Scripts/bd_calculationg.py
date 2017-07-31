#!/usr/bin/python

import numpy


def bd_ssim(r1, ssim1, r2, ssim2):
    pass


def bd_psnr(r1, psnr1, r2, psnr2):
    lr1 = numpy.log(r1)
    lr2 = numpy.log(r2)

    p1 = numpy.polyfit(lr1, psnr1, 3)
    p2 = numpy.polyfit(lr2, psnr2, 3)

    # integration interval
    min_int = max(min(lr1), min(lr2))
    max_int = min(max(lr1), max(lr2))

    # find integral
    p_int1 = numpy.polyint(p1)
    p_int2 = numpy.polyint(p2)

    int1 = numpy.polyval(p_int1, max_int) - numpy.polyval(p_int1, min_int)
    int2 = numpy.polyval(p_int2, max_int) - numpy.polyval(p_int2, min_int)

    # find avg diff
    avg_diff = (int2-int1)/(max_int-min_int)

    return avg_diff


def bd_rate(r1, psnr1, r2, psnr2):
    lr1 = numpy.log(r1)
    lr2 = numpy.log(r2)

    # rate method
    p1 = numpy.polyfit(psnr1, lr1, 3)
    p2 = numpy.polyfit(psnr2, lr2, 3)

    # integration interval
    min_int = max(min(psnr1), min(psnr2))
    max_int = min(max(psnr1), max(psnr2))

    # find integral
    p_int1 = numpy.polyint(p1)
    p_int2 = numpy.polyint(p2)

    int1 = numpy.polyval(p_int1, max_int) - numpy.polyval(p_int1, min_int)
    int2 = numpy.polyval(p_int2, max_int) - numpy.polyval(p_int2, min_int)

    # find avg diff
    avg_exp_diff = (int2-int1)/(max_int-min_int)
    avg_diff = (numpy.exp(avg_exp_diff)-1)*100
    return avg_diff
