# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/pnp/8165.NodeIDAllocationData.2.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.211172 UTC
# Is deprecated: no
# Fixed port ID: 8165
# Full name:     uavcan.pnp.NodeIDAllocationData
# Version:       2.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import uavcan.node


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class NodeIDAllocationData_2_0(_dsdl_.FixedPortCompositeObject):
    """
    Generated property settings use relaxed type signatures, accepting a large variety of
    possible representations of the value, which are automatically converted to a well-defined
    internal representation. When accessing a property, this strict well-defined internal
    representation is always returned. The implicit strictification enables more precise static
    type analysis.

    The value returned by the __repr__() method may be invariant to some of the field values,
    and its format is not guaranteed to be stable. Therefore, the returned string representation
    can be used only for displaying purposes; any kind of automation build on top of that will
    be fragile and prone to mismaintenance.
    """
    def __init__(self,
                 node_id:   _ty_.Optional[uavcan.node.ID_1_0] = None,
                 unique_id: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]] = None) -> None:
        """
        uavcan.pnp.NodeIDAllocationData.2.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param node_id:   uavcan.node.ID.1.0 node_id
        :param unique_id: saturated uint8[16] unique_id
        """
        self._node_id:   uavcan.node.ID_1_0
        self._unique_id: _np_.ndarray

        if node_id is None:
            self.node_id = uavcan.node.ID_1_0()
        elif isinstance(node_id, uavcan.node.ID_1_0):
            self.node_id = node_id
        else:
            raise ValueError(f'node_id: expected uavcan.node.ID_1_0 '
                             f'got {type(node_id).__name__}')

        if unique_id is None:
            self.unique_id = _np_.zeros(16, _np_.uint8)
        else:
            if isinstance(unique_id, (bytes, bytearray)) and len(unique_id) == 16:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._unique_id = _np_.frombuffer(unique_id, _np_.uint8)
            elif isinstance(unique_id, _np_.ndarray) and unique_id.dtype == _np_.uint8 and unique_id.ndim == 1 and unique_id.size == 16:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._unique_id = unique_id
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                unique_id = _np_.array(unique_id, _np_.uint8).flatten()
                if not unique_id.size == 16:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'unique_id: invalid array length: not {unique_id.size} == 16')
                self._unique_id = unique_id
            assert isinstance(self._unique_id, _np_.ndarray)
            assert self._unique_id.dtype == _np_.uint8
            assert self._unique_id.ndim == 1
            assert len(self._unique_id) == 16

    @property
    def node_id(self) -> uavcan.node.ID_1_0:
        """
        uavcan.node.ID.1.0 node_id
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._node_id

    @node_id.setter
    def node_id(self, x: uavcan.node.ID_1_0) -> None:
        if isinstance(x, uavcan.node.ID_1_0):
            self._node_id = x
        else:
            raise ValueError(f'node_id: expected uavcan.node.ID_1_0 got {type(x).__name__}')

    @property
    def unique_id(self) -> _np_.ndarray:
        """
        saturated uint8[16] unique_id
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._unique_id

    @unique_id.setter
    def unique_id(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray]) -> None:
        if isinstance(x, (bytes, bytearray)) and len(x) == 16:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._unique_id = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size == 16:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._unique_id = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size == 16:  # Length cannot be checked before casting and flattening
                raise ValueError(f'unique_id: invalid array length: not {x.size} == 16')
            self._unique_id = x
        assert isinstance(self._unique_id, _np_.ndarray)
        assert self._unique_id.dtype == _np_.uint8
        assert self._unique_id.ndim == 1
        assert len(self._unique_id) == 16

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: NodeIDAllocationData_2_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.node_id._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        assert len(self.unique_id) == 16, 'self.unique_id: saturated uint8[16]'
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.unique_id)
        _ser_.pad_to_alignment(8)
        assert 144 <= (_ser_.current_bit_length - _base_offset_) <= 144, \
            'Bad serialization of uavcan.pnp.NodeIDAllocationData.2.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: NodeIDAllocationData_2_0._DeserializerTypeVar_) -> NodeIDAllocationData_2_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "node_id"
        _des_.pad_to_alignment(8)
        _f0_ = uavcan.node.ID_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "unique_id"
        _f1_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, 16)
        assert len(_f1_) == 16, 'saturated uint8[16]'
        self = NodeIDAllocationData_2_0(
            node_id=_f0_,
            unique_id=_f1_)
        _des_.pad_to_alignment(8)
        assert 144 <= (_des_.consumed_bit_length - _base_offset_) <= 144, \
            'Bad deserialization of uavcan.pnp.NodeIDAllocationData.2.0'
        assert isinstance(self, NodeIDAllocationData_2_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'node_id=%s' % self.node_id,
            'unique_id=%s' % _np_.array2string(self.unique_id, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.pnp.NodeIDAllocationData.2.0({_o_0_})'

    _FIXED_PORT_ID_ = 8165
    _EXTENT_BYTES_ = 48

    _MODEL_: _pydsdl_.DelimitedType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{^XCTaO&abzUw>an+<~>P9J&Ew$H<xNFZ2FOp@NOzf;g(qc9wC5pPhfHA0<u9<FbPj{!QduK<00r??;1PqV`JOTWe'
        'r@)U!;0M12dGk;39|+)o5I^SJs=K;pW=RJTBvsE$ch#v==bZ05r>ghMQ~&z!ch=~i*_+ukFhShy8J$Nej=oU+Sa*AabeyFoD)fBz'
        '+$|kPW4H_+O*1|J)qMMx^Iy!jX3zAZB+>aiT$?@jagmpUqRe&kmeajNjiHM-OLZ_%NjFQf?)@~-cW>>+aXL^%lqR=Sq2{xV-hs{y'
        'e8ld~d@9$!n(wXet^M=-m-E@#o+^qw>X(H!^PfZCD+I6Zn$J$(iF6#)(s;c9#_AO)Vt9tX487TT5iSA2x_58Q!*k*Jy%Ria`25f3'
        ';mdOCtE<M$a@0?B0As%RNn)Z=qJz6hp+`Dz>f>y$9~He=C!->q?_B_i2Fet@F^oJ9zdgJ7q3sAC>%I@a-NT<i4Qu~2e>k7L)H8)j'
        '0+k1DM_-kFn8xV?6_+5vsa}u{=CieV*;lg{9j*2HQ(lf=%)_1VO#{*dI?FXIgAV3j&(8OT(V-4{S(+EUD45@$J>N5FnGZDl5bIv1'
        'V653Emy2<Bd8+oyVh44x^TjxM=i0%Q_;ObE<7m*!^{9-o%UauJXAD!(`DNDhWz_WLySKVmyH~pW6)3J3Dg$HWIw?@S2hl*!zYe>z'
        '|GcG#QKF5ne0**Pp7S1s+8?XKXk3ncn06HSG<iQVK1@j`0d(T0iC@5dC49=`X_SooB3FsQ>G`pm>b&cHicc9oPA58tn^odpy>{IP'
        '8GIE_)YM4l!!(C4;`({h^&aXWK9kZICewpx7_mXq?c)?WiIQR3#TDttW<Gn%8c)4+Fwvs@c|JS$UR3-8ef}6eit)@&_R?%V^H+6Z'
        'rsIAJ`Ug$k)8iCO6J>dj>0A|Q?t1MYjKC|xpUl4Tp$Y=f%fe0JE&TO<8OJK0wts~l*wX%GzO{GZ$n?Q?Gwx`<w^8<Cy5lH8>xK(;'
        'h!<zj!oeu8@4XZF+}hFJy0j;;J#n;mN<N>K&(C0c>S*r_w(CcG8}j?J*q%As^RRv9Xzwhxr;ql|$^Fk^d-7=Sygc^}>F<I(|2)gR'
        '_ky%9O8b(uFH3t-+E=7~RocIj_BCl=m-d^|eoNXnq<vFbU)pa=yD9B=r2Ve6e=Y4>(q58wOWJK|zbEbYrR_+&BW+jO%hFzv_Nuhk'
        'q<vf3cclG+wC_s$Lus!|`y**@NPAP-zmfKDrTwwAKauwDr2RnJ&!r8eJ(Tt<X@4#4Z>0Ubw11HHkJA20+COu9Z{vhqylOAD?8S9^'
        '@qxYg++KwC;?Q1vWiNhhFMeY$es3@SU@!h?FaBgN{wx<I1bKa!LEu0@lkfVbPci!pMl_7IVfXW&om^YHJEU+j*2buj=6Hi)2I87Z'
        '(quYLOXF`vUES?qKoSJ?bN!DH#)|C@JPo(Pzt{_ec6c_|fsY~cn69Dco#VTQpqCik>R;}V{_OzvTkQv_#=Z+bR0r^VG8Kt*GSD4A'
        'Dtr^BWgJ-P>FF>Ug?J6z!$g3sRmk`Ew9X))`Vd<J4Aq5)_ZO42dPZ(#C@>VoL2^J6%@I7&aCg2Bz!3p9Ckn)X_?^b)rWJuOB20~D'
        't$-ML8b*DjJ{=D*)SX~Tssr>)$72MX0I@(FqyQHq(5>_Z<6F5perfQ_M1y1?t~yXrjQm01M-VIlpi}`vTs_nzV)#Llq+Ky^eG2LY'
        'm_bgX4)b)}G61WZGMfN*=y)Z_7XzRUb6v@Y(;23Kmi|_n)APe92RY%Fr&A;ALk&V5Y?HmU`XA70qgwl#N9wc`O0z`ez)TodL05zD'
        'm>GFNI!S0w{;_lF0vmF8-0Lg2W1g!iu&g`CgBXE#@vA0@d#<NrJw}?sO!7O@?OS^r;id5VVF&ow>{(!TnHogJ6aX;19^Ryz!XJmb'
        '4#d9j5XedqEeGoL-abBhEBt$Y^d82JjU$R2AMSk_egywLTnVV_EkHdffV#c{P}c=eHv~}62%v5Vpq_03>P8DtpA|q|7eGBPfVv@o'
        'x-NkFf&l7s0;n4Ts3!$bUll-osRgL#1W-2wP)`Y<t_h%iO91sX0n}FnP+t;2eO>_dya4K10n`lv)YAf}>jJ3X6F}V(Kz&O9^}7P7'
        'n*yl50O}h8sNWPoeN6!MRRPqC0;n$upuW%o)bj$U=LAqa0n`lv)Mo@xPYIx|3!ttYmEmvk;>#LUo-LCI;+f#ekJi`L9uW`5FVQK|'
        'R;2FwkDRdn@$S9b5{xj+vR5PN1+P1Zl<#IsKh?!u<hT^ADhh7O{$o8TI3$uAL)HPlT;Rw9KoSUK5IZ35>h7pZPyjt%qPQ>s5<Y?_'
        'CqPm;(BVKNM42QI-a4Kl0FYjJP(hMD&N7bnbv(tP@uPvh`cpz5#EKvq5&|(=AgWF$p(d(MeL`f50}E!X6V<}U3OSDj%1XJ0quN*%'
        '5Xh)c7FmrH#(Eqz$~}l;^#Z}uFh$5BF^6zLJEDcl1)jLit}noQ_m<&rD5@qB!F9~B5{v;=U*Mo#6TKU_Ng<xZqy>hsslzK6ul^&v'
        '`1rXKYir@}%JACP;oJBA`_1s3+5Z1SHkc*Z<?C19{lU`8K=)dmBZlunKKS|nybU}l@zXru{0ml@@DDCi3Zk@_%Kv2d)Ax7pTe#{-'
        '`Us|inH*D+YU<X|c?n>}Km)8nc^oW!nn8XS$5ZTy)4~eaAa6v|O_O0XDiNK=Dk<?^(k4P8-Fwpy0qFt4J1F5m=eQbZqR@lU?0x*C'
        'r!t@(_#6nOBV2UKV@;IPT#<Z?El29GQ4G;qWYU48%$8E^#4v2^54FM?4Z2|#mm@IhU?+oA*kflPEudXYjJOBtv`<p1mYJxsNWt1z'
        'CBQ4d`eFVFxIHnFw4przGc-tGN_~(j@KC*V2Ywb#4fexHd8I~nsV!527L=j;eV}4Kt#F_V9?Ei3J2eqMO~@cXNetEQ3~{+0r%P;v'
        ');$H9$6PhSG@h2DCDR0YF)1!&*Z;Vb#kGV}_(_p^AoONK&3xY`@vF@blMn4@G?IR<4}dHHaiUmir-L(tg;zKS(lo{*oO}*EI5Ma{'
        'iWSChhCL9spngp{78A&I9I1X3!zjL)f&-4tO^O6)R-*)nCFp@;_5h|bEO9uD))6^cNI3(TKsp>kTuctq7#U%o?Jm%RC?Lw4f)3z8'
        'D!$a~()I4A`Iy}Y=pD*!?Fn!JX{&L9ct!I_8_w$D9JH~O9T0AyGeVWkIzG2E9JAR0YuC!q1E!1%T4(A(*1xLjcx-};<s48suyrG='
        '1HL(cQ5O8Dnv;VGQb-bo8A2h7g7`EUzzvYzQeYGopbu<{7`L~W<N<2pif`5cQ$1o6DQj9N2~p>|`>wy+Hu^EhUHb{4Mv6{^tJ$!7'
        'lDO{bhUfYIj{h^Ar_Q$&+E^S6YERY=c%!5Qh}9if+gKchmx-+fEeD44-5~3RU(CWFc%wqPEZ2j?$t>DZ6^@HN%_0(n_c7N)->Nb<'
        'k|-LsvX~)Rihox;prJ#~c=9yXEfxmP35)=SfyIqsf)HU6A}>CK8lFBd464ZPR5S|iV{h&Vn^Krh?m$Wksqz2}6+j=xi?Q5Eig^@b'
        'g0y<Y8bTR6bxB?oa=|!a;;@i{B0W?jX8^H@%g#hQj0VSp2pNyk92RwatahwnqCN`H6a{?zAx_!nAh^>Ywd&9#aH3ICQrsu!SyCY}'
        'LUo(*9Dj^*ZQ4_Z7>>hGqKg<9s~qAA@))p6+3zqym^1}XV^{SF^Jj*Ko>xJ)EH6m{YBn*%>;hbY3dttTLW=f^I~-?aL9zojfz1|Z'
        'F!lOVxL<7mccO#V`WKe_6Qx#sT{P`vL1zb%o}dx*Q|L|~QY0pPb=HtwcGWs!D0I|~DuFr1@l!4(uylt8jv&2IZs<cDJJqNL?;FKw'
        'pNR_-zN^=+?;y8`c+<v@a03Al0IAx3g5+EouTG%0IA_>wb+ZZB13*%10dS&kAs6NggA+u;w2#R?_;C;yY@%9|dTeCodIZ)1)NhKe'
        'zTHgUoUEu~wU`7&Zbncgh?TvfQ6nsQ%hEd^IC-U7BdRoIMq4Rdr=k6tWw{}nI@~ms=Sqn&D5#@T7I}h1(W%BQ1Joq2w_&zrSqFA0'
        'Lsll@Z*jVWj;0U6fxMKdG!lf$S6ec4e5v$-b|VPWWq}OH-fRYtWY`a=5?JE`d@M%hcB{-ONLIpjS|w2jreMJe<BTm+sQqn=H=V3^'
        '$of%;MjZA40+AUe#VQ}&w!DDSK~y_fI1B?42jxJMdtjOYOcy<KNgmtvKe6(8PE~auT^(_0LAuR0By2*wQLT_EEL@UN$$GL3HP?r*'
        'p>^Vzg-!McY3{6dv($?Yu%sYLx%&j-EpS#O6-%X1iAO(Di9V1_1(F>-ah9#Jr&fSzuAr2I^Pu*&woF{SVDIT0?6qD#H@4LkPmaiy'
        'Bo>XO9$OJvx~-uV4v#GYNB1u=8~_1KXPhOiP|wtuU-^I|Q#CbjYayKyY9}krNJg8iX|hB$Fv>{fK`g|YP^299!Cf1))7QXN(<#-M'
        'KdXvF|JTK5x;e_ziG@K%plbgC{AChlG>FGNBl^aWfx&ZI3ipoD<BdF>>v2kja-rQzm2LAEt0xnUAuCadhV&(#Zg)I@^MULiH2DaU'
        '4Fo#IBnu*e<%~4qu&ff{fh;?8Jz;y0w5iaCg;jFR_Mx{y9%UT3oP-%ehpK8CJ4-0IHA^S`Ma0~6Qa!T?q>pr@j46@cR^<kZ|Mj-J'
        '`y2{6Hky(r;GhHDsDW`nS0yCwu-H?trP^wpX-}r@zb0*u59D4}-6m72nNBg;6M4GcZQ?yn(02$G+J0+)XdE3<cT9DhIf~fq#w`0y'
        'pX-Z>O`N?22a}B1I+zrSD7-kGcYHa%P$T%3ULyClloBK3RbsbuG&UA3J2$oI<Yml&YSa)dY=__$clz+ldSEA|tH=b-!NV$EkY+${'
        'ZxBgkQ=#6lAi<?2rz3&OKC)^q*c8zif*wA*>yF@5=aNQI8XsNA-L@Qcpa5H76x;B7u2lfhaiTb3jEXK%+q<+vv~tdfXyfukj9OR;'
        '2Uc7}8@B^nS>{h<!_{W$SZmpbB;q~55SJs`A3ISBbJ3852CpF-Tmm~dy%4ZiCuABt&^X1)0MQ$5`{ejoG221fSntLH(~?&U*J*oP'
        'q0GKTvT>S3@B@tP*~-7cVvs?YY!zhvyY02(njl6yoGxU>vKsA(Py;21$_xoi9(BvxpDPxt+7`vHF-OTHdqaC@lCxz&f4jBW=`kA~'
        'fSnXt7{@pr?E5fR0AkJyTw$rUZ$q*LNIgMpqlrs6t{78;nBe9Mq_baOv8J*voAnTcF&p9aqubyYV{?nX#@q#K*^tNPRtVRvVJZny'
        '2(&<owL0)x8}c0QDaf;P6l$Lf9Im}kveASDia2ge=3->IxTobUQHa42BETGqQ`XX#WGZ&=9sA;H2dxJwqZ-KA^nf!iuo_R2_MoZ+'
        '7?>Bi0hZMw+ykaXsmr!we~ap}EFNYjSTo`o631PU&`65!MY20((=GuU$;glz`S;VpCV)@2%?_7|S%+g1s4vA<Bs1yIqv6n1{h$s4'
        'KoG%K4VLh8+<GY@{j>#;o3<pIyT|B)bWl>I8@<l6>a228-#JA(h)di<>h5B&3T~q$Qj4ih-sNNJM{2gUsk~LWRHh<gm$XAu2NL$o'
        'z9c%U!U1r;iH_rn)wpJw#cIIWdn>tY)lfO?p@kV6Z9#Dm6KEV!WmTM|3eK*vfga|_WUERR2ogHB^k7TWE`M=mQB|bNjP&o;rRzKu'
        '`J+^NH+O9svQz5{hy?A}VxlJnJ?GJ?`alVLqaL$7r>f@CD)3?KT@h6|qXH^7vAdr2V^r85M+GM_oYeY#1zz1ux3y+Gf3$Q4peY48'
        'a#AcN>CK`TSFods6gZo}7|GB_Erp=r!gPYPdb+@ZtD`|JI*W6~hp0M%ch+2-N~%lJJ%RjWr&gZ;0EW1j*iBU>caL`wWgxc`8**&N'
        'uDa<qO(V_!a?^n5yfjI&?(d#661`Ck{g^s5stF(G<lrwU%vR_lYbJXRRmK;YH0CkU>NsJrq>xX0)v8%xO=tz|6IJp~3sGyXvC$!Q'
        'q*mrbi-T!26$0`K^q1wqIG{6au9j3m)zD}pkkz<4W--}7d4IX0N_eW=WNNT9LQ}{J6_N<>Pots$;%y#NZI$WN2oR(aps6n@2)TB#'
        'wY1>gvXb^vxAj8g-dWc&0kl&NX|7$jQC+gG++KFC(vMT`WcFgx*4@X3kCw;Z5aaOO_}4{^;=Xui5jFj3T3*7yQ092dB}V5`R5PnG'
        '2u}0++R;9WEHnmtvRd_yw}fFMC^uuzO|d3bbe;_L*7Cfkhk7)tW8jEasoqLsKF1*qy|UUQZjH6{2#Ui<Jt?C~Aq~&A<cmAbH(hga'
        'pEzchn$4`a^9;-4m3;CCSzvWEr&d#h`B8ch1+*0p3`E$@NGCdnECqg03+KI->ML^gEmjn)7tjxYwOOj|U`7r3BSvO>GG)mzRCjv<'
        'G($xUJimY=;0{g8<xqvjJ4SarL!1G=Hsd#s&WaJ3c6_873>Z{{8<3sU+b*t|bex=wcTsRX8d+ABW_;MGj_nJl?pm80)oHf6OXuwB'
        'k`5QnZSn4m<CV^izb2K|x&TFbf;Ph(C+MgUePhdL{iGLKgjU-?MX!cA=L6cSWbBca<IGRO5TDL7%c8#2&8wJvr?ETYA_?U35FrjC'
        '72n`<Nx7z47ZYk#=TgOTGpSkXN-IGIX$uhU5sk(P=Q{Y%>q7}eVuMGTc%OC^T;stTD%mmEPw?y$<%huXwmXni*K$w_2%(o4?N-e@'
        'ZJvz3WA-qW!-T>1P5Hg9O5!PkLXW0x^w-pVk$Tl;EUJMIuuqm2kL&?#S3D^NPz90?>gRG6jSnqYWhfWGJ;>fe2s#l~a^wh;JuZfY'
        'F1!&~Pr@N7$Ae(QX|>@R*S!L@%*uS!Dy7#Xpnb|-Hm2+%T7J+niPmy1z6GGcBXHL%QlND@qb0r|C*S<A1lGTUz)Xwo)ZJ~Akcl+x'
        'T<eydS4i&0eh1tv!$yHuB!P55$$hcS33B!YJ4vF9A&!#ZiyP4w*t=)SA;gG?c?O-1V1e-f%DqRQxZT=geDBA~V8wurU0F7Z>m1`g'
        'zPtlkk#(e*5uXD*xVr5zK&gE>ssY3JI1JbW1i1k$940qQvTixUj7hmfQiXNr9A8Z_A+p%&7y+J}vqcAwI!2cL!=3)L&^uHpvmq1X'
        '+D{o~@l+f66-0}4jK}8iC6dHR`CYHfuwEPZTaWB(JI={BA=EhqMT+ECP^zooeBg%x(4JjJR}Q#UNlo_I20BmpOh)r%6*Bn<-6+>>'
        'Yt14E9_*STa7XsDu&PJf%md9nCok`?3MIMX`X8<2kdE~>cAlh^RGnO9aArM;9|KFN3NEZS5BIB3O%2l%{FT!wnbBpCwirdT3}Xt#'
        '2N(;ar<n*VXvD{;s369|5T`;<vCC3RRUfUK5=hsF$Yp`?u?*k78AO??pdIyy?*k#DK#jv1*dnV<4yiz>9p*)g#JOHS#d1N6<|j!U'
        '7_IAY5F$zxvo#Y4i>Bi#>2y+`sl>A=ytg$_rK!s6`0^1l<jhu}i20BpHkJ+2IOgM>7Sz$5uy7s3Q&DIY_3=qGKM`6Vat)NqvYa(m'
        'Jl39_=-4wyt&Q$_53Y$hUbRLTj@ZFaUZhGnpRC9CfoLna8M~`IRDh}Le{2)$dNfLgWHxrf9(oR+i3LtQ&QicC;1CdX=&TT(0<t=('
        'wInzsHPgOM0Ec0j22{8SqLvd!NyuhJL>uC3b+$w{X7Vvk2^9VyX{zfI0)3z@bkIW#5UlYc%+qodwl?kLjSSkmqZ;2sxbk<q{sXKI'
        'f^_s|6bgBRiUe2Nyc`cP5C9n~vYk4Y)2=N%fNys3Qa==JKZ1qJZBT9p29VA!b+;1mJrWS?Dw4ce;%lSFO5)}?@^YDZiUIvCiQ*WI'
        'wpUE3pQkFoclg_eW;+pmEF=$-pjP}|8Ce*^l2g%+U)%7hezqi!vMjNB1G4cd{Ib_E@g<ujZ)0}tkoCDR9@6d*t$uf?v+TgxliwGz'
        'YxzE{Wm9#QzI^t<?T5E<r-b60lNB}I$FcQRn~X1e9mh`ZxPNx<--7>dEjuGu@4Pi#uF}f(3Trb(nwb@rQ#qKN1gnoyNTP>nON84m'
        'a-0WydAr>U?<iHr$;2Tu`x3^YRz;k5y8i7$+{JeG6Cn4i4y;KzRL*KFEe%ZCCp8Hw>au>(b}nOIJ8i6XGf7xTKyW+6ZfJMs%U`6t'
        'Q(d_)SHAo{@F9gM#j^J+@dZu%I|yL^_}4_1_V!-*VDALIZFwR52>yEr<No$OeDPn};I~Kc?NR;h1N`d;3t#g)dEwdcTzCQhn#fjo'
        'G5p<e?^Hd$fZyP&PLH35tJ#^JK18sY-}~~!>|!sFKgN>xLdYMWX}^T(hnK?by%YHNLg-c0r8;~3I&@7R9=`!sD3<%0sec3$bd~wa'
        'Lu91Ky{`I9Z=e6%!<AL9tgeM0!4yz2_SI8E8e(Po@aw-V`4u1T{xANuC?c^&000'
    )
    assert isinstance(_MODEL_, _pydsdl_.DelimitedType)
