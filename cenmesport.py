#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: jeremiah.marks
# @Date:   2015-12-29 15:34:21
# @Last Modified by:   jeremiah.marks
# @Last Modified time: 2015-12-29 15:34:33

portals={
    "id1451375395373": {"guid": "97c96633ea454a30a62ee451a3e238a3.12","lat": 33.437024, "lon": -111.831583, "label": "Irrigation"},
    "id1451375400374": {"guid": "083c82cc56e14d1cb8dca83d9541fbef.16","lat": 33.437112, "lon": -111.814763, "label": "Park At Canal Intersection"},
    "id1451375417376": {"guid": "b403e76a75264bd0b86b7a9e9fd24288.16","lat": 33.433855, "lon": -111.814134, "label": "Desert Heritage Church"},
    "id1451375420681": {"guid": "5a9e139d53b846a59a6fe9508e6c25dd.16","lat": 33.435664, "lon": -111.810914, "label": "Church of Jesus Christ of Latter Day Saints"},
    "id1451375424673": {"guid": "7d7471c27bdc42419565b7f9cddddbb1.11","lat": 33.436773, "lon": -111.804965, "label": "White Stone Horse"},
    "id1451375427992": {"guid": "c387c20252a6418ea884b42d0e5fd207.16","lat": 33.437165, "lon": -111.802515, "label": "Lakeside Waterfall"},
    "id1451375445460": {"guid": "2f1e68f39d774beb9f65d5a27a3f8adb.16","lat": 33.43246, "lon": -111.81413, "label": "Kino Aquatic Complex"},
    "id1451375448121": {"guid": "4afa95aa9821437faac1f8216bb50de4.16","lat": 33.431353, "lon": -111.804993, "label": "First Southern Baptist Church"},
    "id1451375450950": {"guid": "ab337911c72147479e4eb2dc4c3a7f9d.16","lat": 33.431272, "lon": -111.803923, "label": "Learning Foundation"},
    "id1451375454025": {"guid": "892a2243e9774958b471545b7cf5287f.16","lat": 33.430461, "lon": -111.805072, "label": "St. Lukes Chapel"},
    "id1451375456914": {"guid": "65c20575794d43c9a048ebbbef883dda.16","lat": 33.428154, "lon": -111.805101, "label": "Church of the Redeemer"},
    "id1451375460133": {"guid": "a9a6ccd66068467c8491f7667a87af0e.16","lat": 33.425385, "lon": -111.804928, "label": "Abstract Tile Mosaic"},
    "id1451375467083": {"guid": "50b6b7c5d2484ba99763003267c5810d.16","lat": 33.430359, "lon": -111.82222, "label": "Porter Park Dino Mural"},
    "id1451375470209": {"guid": "13f7524fc4fe4b508f63c2445a56676c.16","lat": 33.430081, "lon": -111.821709, "label": "Porter Park"},
    "id1451375473639": {"guid": "0f530b64d8984b04b3b171e6496abbe7.16","lat": 33.429678, "lon": -111.822945, "label": "Fitch Park"},
    "id1451375477735": {"guid": "220cc0f042154606bb885cc8e4f4a5b9.16","lat": 33.422957, "lon": -111.804557, "label": "Circle K 415 N Stapley Dr"},
    "id1451375480344": {"guid": "4decdba615174d18a6c561253fee2831.16","lat": 33.421938, "lon": -111.801717, "label": "LDS on Lazona"},
    "id1451375484857": {"guid": "1145dac451874dfa8ffbf49721aa9aca.16","lat": 33.422115, "lon": -111.810055, "label": "Church of Nazarene"},
    "id1451375490267": {"guid": "76a7c626b16641599b9ba4b4c22892a6.16","lat": 33.422219, "lon": -111.816445, "label": "City of Grace Church"},
    "id1451375493260": {"guid": "94570a575c86429c99d2979630202c39.16","lat": 33.422459, "lon": -111.817004, "label": "Joes Fountain"},
    "id1451375497900": {"guid": "88681e2744824d72ac3fe746681292b8.16","lat": 33.422475, "lon": -111.819465, "label": "White Lotus"},
    "id1451375502787": {"guid": "80a80b3a3d534764be970fd830d48198.16","lat": 33.42258, "lon": -111.819731, "label": "Green Tree, White Fence"},
    "id1451375506869": {"guid": "ce012a63d95145699413b089a839b8fb.16","lat": 33.422703, "lon": -111.822235, "label": "LDS Church"},
    "id1451375509511": {"guid": "eb4af5986bf54ded9e5deb1ec7761b5c.16","lat": 33.423841, "lon": -111.824369, "label": "Mesa Commons North "},
    "id1451375512617": {"guid": "24e8a6ff24b24b25aa870f0e1d59ef8f.16","lat": 33.424771, "lon": -111.826299, "label": "Escobedo Playground"},
    "id1451375515675": {"guid": "a9f2b73433d646f4bf148f099727204b.16","lat": 33.424713, "lon": -111.827018, "label": "Escobedo Park South "},
    "id1451375519948": {"guid": "4dda5ce9fa7d43dd83dde49ce9dcdc00.16","lat": 33.421914, "lon": -111.823408, "label": "Circle K 310 N Mesa Drive"},
    "id1451375525759": {"guid": "2910c1185dd5400d917f93f49aa728ad.16","lat": 33.421459, "lon": -111.833798, "label": "Mesa Active Adult Center"},
    "id1451375530914": {"guid": "d12813a0dc7546f8899a4c557bb6fc05.16","lat": 33.422483, "lon": -111.830449, "label": "Iglesias Pentecostal"},
    "id1451375533673": {"guid": "ae46c26b00b04fa1ae3ac4f082806881.12","lat": 33.423091, "lon": -111.829726, "label": "Calvary Servanthood Korean Chu"},
    "id1451375541953": {"guid": "a884329a837e44d88adada660b52409a.16","lat": 33.424009, "lon": -111.829084, "label": "Christ Mural"},
    "id1451375544963": {"guid": "d4da2897fafe48c79a63d2014b8bb583.16","lat": 33.423828, "lon": -111.83022, "label": "Washington Escobedo Wall Art"},
    "id1451375548256": {"guid": "51f9551a61cb47109c3362cd3dbda981.16","lat": 33.424067, "lon": -111.830438, "label": "Washington Park"},
    "id1451375551507": {"guid": "d42361279342477e8838b433df7949e1.16","lat": 33.424061, "lon": -111.830704, "label": "Pentecostal Church: Brazos Abiertos"},
    "id1451375554739": {"guid": "87548606db0d44d79fe50c63899b0744.16","lat": 33.42438, "lon": -111.831733, "label": "Barnhart Art Hause"},
    "id1451375558654": {"guid": "e96fe3f0042e44418dd95dd5f30e3ea0.16","lat": 33.4229, "lon": -111.831897, "label": "Circle K 410 N Center"},
    "id1451375564177": {"guid": "62564b0fd99e41eebfe4446b8b120672.16","lat": 33.425376, "lon": -111.831617, "label": "Voice of Pentecost"},
    "id1451375567179": {"guid": "eedef24b1ef2442292440ca87e7dd43b.16","lat": 33.425821, "lon": -111.827011, "label": "Escobedo Park"},
    "id1451375571696": {"guid": "a58d20afa86f494db6539d8e615a7431.16","lat": 33.427213, "lon": -111.829943, "label": "Fitch Baseball Park"},
    "id1451375575128": {"guid": "3b4c95c5e97943b18bd389f37007e509.16","lat": 33.427072, "lon": -111.831198, "label": "Fitch Park South Entrance"},
    "id1451375578694": {"guid": "766429a80f3c42e8b6bce4db9605eca0.16","lat": 33.428518, "lon": -111.831811, "label": "Masonic Lodge"},
    "id1451375582380": {"guid": "880a3871fa87493aa23fed39ae7a5ddf.16","lat": 33.429506, "lon": -111.831166, "label": "Fitch Park"},
    "id1451375587230": {"guid": "dfbef8d4a2274baba3e5282078e86845.16","lat": 33.435486, "lon": -111.824907, "label": "Grand Fountain"}
}
