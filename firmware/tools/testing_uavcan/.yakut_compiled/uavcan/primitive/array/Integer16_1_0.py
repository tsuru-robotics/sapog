# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/primitive/array/Integer16.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.684480 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.primitive.array.Integer16
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Integer16_1_0(_dsdl_.CompositeObject):
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
                 value: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int]]] = None) -> None:
        """
        uavcan.primitive.array.Integer16.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value: saturated int16[<=128] value
        """
        self._value: _np_.ndarray

        if value is None:
            self.value = _np_.array([], _np_.int16)
        else:
            if isinstance(value, _np_.ndarray) and value.dtype == _np_.int16 and value.ndim == 1 and value.size <= 128:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._value = value
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                value = _np_.array(value, _np_.int16).flatten()
                if not value.size <= 128:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'value: invalid array length: not {value.size} <= 128')
                self._value = value
            assert isinstance(self._value, _np_.ndarray)
            assert self._value.dtype == _np_.int16
            assert self._value.ndim == 1
            assert len(self._value) <= 128

    @property
    def value(self) -> _np_.ndarray:
        """
        saturated int16[<=128] value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.int16 and x.ndim == 1 and x.size <= 128:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._value = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.int16).flatten()
            if not x.size <= 128:  # Length cannot be checked before casting and flattening
                raise ValueError(f'value: invalid array length: not {x.size} <= 128')
            self._value = x
        assert isinstance(self._value, _np_.ndarray)
        assert self._value.dtype == _np_.int16
        assert self._value.ndim == 1
        assert len(self._value) <= 128

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Integer16_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.value) <= 128, 'self.value: saturated int16[<=128]'
        _ser_.add_aligned_u8(len(self.value))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.value)
        _ser_.pad_to_alignment(8)
        assert 8 <= (_ser_.current_bit_length - _base_offset_) <= 2056, \
            'Bad serialization of uavcan.primitive.array.Integer16.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Integer16_1_0._DeserializerTypeVar_) -> Integer16_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u8()
        assert _len0_ >= 0
        if _len0_ > 128:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 128')
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.int16, _len0_)
        assert len(_f0_) <= 128, 'saturated int16[<=128]'
        self = Integer16_1_0(
            value=_f0_)
        _des_.pad_to_alignment(8)
        assert 8 <= (_des_.consumed_bit_length - _base_offset_) <= 2056, \
            'Bad deserialization of uavcan.primitive.array.Integer16.1.0'
        assert isinstance(self, Integer16_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % _np_.array2string(self.value, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.primitive.array.Integer16.1.0({_o_0_})'

    _EXTENT_BYTES_ = 257

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{`t<OKcn073KVC%OA?}N3oNbacqZ99Fj`>VVqCZ1T9qD9#^&6K$~JTB*&UT`56p{Dit7wvS^_I1M~qI16pdSrIuQ1'
        'sil@`yU|ihEw$_&l9H^*vMpPZ(N+Q>&U^RXbI-f)@li*2N_{etPPBi*tKMX}QLbdohV8pn#r@7IR_v@<s#m>w!wu{xJUtTl%~H_x'
        '?LSO<cJxzp>xbz3C=+UC&8o6J-Lxi3RxRuKZq*Ik2|H`~zBQTsO)ap;ZGYfi6ei6H+i$q_TI3``<J<1@PZ3F!_<Qt26!w@_5cqDf'
        '8Q6{JPtjhiww$6+`?YIV%G+#Cnq@1n%pj&1UfCl&<`spPzO{IkXMStf#slY<@$Al}oi^=?UA1dL7jF+bTPu#j-Vt}aW|zBb-ig*@'
        '7Tv(Cw39`YVyY#p5t!9_*^Zpc;l<%im^du^4cic#xIBr!MUSHJyx9n>TG{f;PXkRii{S}I@~n~@Ohz;np6i;-$8l*o)EU3;kG000'
        '<eaONbkfc>lHyd(jTlumi<L$c-rQXDc2Zt{@bhsLp8DDiI;9-pVHY`6%(};iV=s`#WVKkYxTPrUgI%q2NdrC;zw>P03hMrL@pQA~'
        'xV+KM-SEOU^;*da?AkM3<6^{~zFp%Jlwtp~51W;W<xlSN)XfR2(zK(0L>WqoM$x(7Eye?my7b7ZjoXiG&ko$ZDE-;2S}iU)2YlV0'
        'bbb|Mr5LMSzp7i~&5Iw{4T)rE#Jk<BSaCc_v2Q|<+<jNt@BCSi1*zRRZEKDcQU&Rqu^c}eJ8YzpE-2ZJJF&|~2CtD$ZpHHqk9(f!'
        'M<?i{pi>=NGR}2+Pe1CRQ-aRyz~xz<JNw)iI!$K;rMi53U+7C`xvq3>S01+TeBVpOQ!kwpbiU)Ovi(#Xd*P*HsgKSJy7){EY-QV}'
        'ePPiBx+ti>6O)Sf<E?$i(<SN`ba_us?7{XcuY^l)(Pcqz@2D4B8SkA}#-l6rwxD;P%a^^_=jv<apm*q9LFsO71-<v$Xmpj*g06LN'
        '($C`_XMX=c^3i*AP0;ntoKNjRT%j8WmV@4>>w<2+a921Y&ED+$!GY$c8+21pW^<iMj^tBz>%eo+2b2-?;Y+WRBiR3=L*YTU=tDub'
        'xA*osV`iS--;WP1FMUL}1!ebD2ae*H+@W%!k0~oCzj-6_=WXE7^HGlSf<D=IEjW_nK0OkCG(evSy0iPN+-B_j=6Sh$WL)S|x+Cb`'
        'E7gpnIrjdMa;3X;Pf%g|e#x}!#&^tTN6v%pQ$f&!SFRl+aQx?Qgg1Rg4+MR&_c^@7ISTPv{PK<QqtEFJL0`RAeHn!@e(^@vKwr{V'
        'f(EzlLcVR9EE?^WXVu!mxots0MnXkGXMI5_q-3O2q;yInEhDWWty3O(8F>|Xodz)|V^GDQPQw_MF|1-(r!kDl7*jE(lLt?Rr^3@|'
        '3R5zsR7~k4AY=#?LZ?~G%9vF#tJ6H@Wz4IX*J%-pG8R=V>a>hy8Oth`by~%$j8zq@I;~?}#=44i<|!eeAfX{)ASEHCAf+K?AT1%S'
        'Agv*7ATJ@WAg>{BU{J!Kf<X;~28JaJD;U-=Y+y{nn1V44V+K44o&ryUXJAUgl!7S@QwD?tp+IO524*G9Dwx$UYhYf&yn=ZR^9B|r'
        'EGk&kuxMae!m@&84a){rC9En~)v#({UBbG8bq(u=XcleOioa*U{0PaUGxA@f<&yDV@rSJClE+%EUFX!XmOB(Jmy8)7sFq8==v(3t'
        'v|M`U9{kU0xpe#gNB>`1E?)EX_U;~QxlJv{pW3+g$6D@ZT5jiAIo5Lf)pDKtCBwGVv6g!cE!X)zI@WSWq2=0lA@6$AdD0#tDI=+~'
        'l0Z_$hK7C_{W|rdpGO8|kdcv5k<qDuf{KESf=)vik};%WNT*SZ${1BKs*?jphNHsK(c+g(Ewogc#<YxS71KJ+U`ED_iW!~eFehV9'
        '#hgwHSdg)xVnL@REXi0>v82-qR%EQGSkY+>YckeUtm)WbQaWv5gE>n`DoAQb8t9kMub`jF8_4iWLPkMGLqS48L4h9(3`rPLFr;C~'
        'z^H^#1)~~94LA}U1&#*CKubbPK}$o+z_f&E1=AX)4a`WGQ81%n#=x9}IR$eX<_s)ISWvK_VZp$Xge3(_8kP*KNLW#@qG83rhJrN-'
        'Yy4Zo8V@BFaB+Xm(L$}${|i;KTrWjoB5D?`u<xlJv{{_&bhp2coPRpKjj+co+n#U7?Z<NTV|d1V?6&N(>DB$fbj#7hu-9zVn|{e='
        'L&Y{dD{!LluQ{h)wQ~)(GGY6<?>I>-*RZ_$c<!<5SN~%9b}p#bD~%jy4BXnd+3BR`yk@cDmQ3FsZ&u=j+pX<JZqsG6XPj#{wR2m|'
        '_Uu45pY1qByd=kJFd08?WjAbp!Y$d+kIuiGe>+)cpwqd$v!nZYcGxPHnaZxNCtC|)lCj$6h?32nQrLO&uv6abe*paQ*^FKw000'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)
