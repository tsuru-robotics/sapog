# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/diagnostic/8184.Record.1.1.uavcan
#
# Generated at:  2021-09-29 15:15:51.627723 UTC
# Is deprecated: no
# Fixed port ID: 8184
# Full name:     uavcan.diagnostic.Record
# Version:       1.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import uavcan.diagnostic
import uavcan.time


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Record_1_1(_dsdl_.FixedPortCompositeObject):
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
                 timestamp: _ty_.Optional[uavcan.time.SynchronizedTimestamp_1_0] = None,
                 severity:  _ty_.Optional[uavcan.diagnostic.Severity_1_0] = None,
                 text:      _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]] = None) -> None:
        """
        uavcan.diagnostic.Record.1.1
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param timestamp: uavcan.time.SynchronizedTimestamp.1.0 timestamp
        :param severity:  uavcan.diagnostic.Severity.1.0 severity
        :param text:      saturated uint8[<=255] text
        """
        self._timestamp: uavcan.time.SynchronizedTimestamp_1_0
        self._severity:  uavcan.diagnostic.Severity_1_0
        self._text:      _np_.ndarray

        if timestamp is None:
            self.timestamp = uavcan.time.SynchronizedTimestamp_1_0()
        elif isinstance(timestamp, uavcan.time.SynchronizedTimestamp_1_0):
            self.timestamp = timestamp
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 '
                             f'got {type(timestamp).__name__}')

        if severity is None:
            self.severity = uavcan.diagnostic.Severity_1_0()
        elif isinstance(severity, uavcan.diagnostic.Severity_1_0):
            self.severity = severity
        else:
            raise ValueError(f'severity: expected uavcan.diagnostic.Severity_1_0 '
                             f'got {type(severity).__name__}')

        if text is None:
            self.text = _np_.array([], _np_.uint8)
        else:
            text = text.encode() if isinstance(text, str) else text  # Implicit string encoding
            if isinstance(text, (bytes, bytearray)) and len(text) <= 255:
                # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
                # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
                self._text = _np_.frombuffer(text, _np_.uint8)
            elif isinstance(text, _np_.ndarray) and text.dtype == _np_.uint8 and text.ndim == 1 and text.size <= 255:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._text = text
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                text = _np_.array(text, _np_.uint8).flatten()
                if not text.size <= 255:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'text: invalid array length: not {text.size} <= 255')
                self._text = text
            assert isinstance(self._text, _np_.ndarray)
            assert self._text.dtype == _np_.uint8
            assert self._text.ndim == 1
            assert len(self._text) <= 255

    @property
    def timestamp(self) -> uavcan.time.SynchronizedTimestamp_1_0:
        """
        uavcan.time.SynchronizedTimestamp.1.0 timestamp
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, x: uavcan.time.SynchronizedTimestamp_1_0) -> None:
        if isinstance(x, uavcan.time.SynchronizedTimestamp_1_0):
            self._timestamp = x
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 got {type(x).__name__}')

    @property
    def severity(self) -> uavcan.diagnostic.Severity_1_0:
        """
        uavcan.diagnostic.Severity.1.0 severity
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._severity

    @severity.setter
    def severity(self, x: uavcan.diagnostic.Severity_1_0) -> None:
        if isinstance(x, uavcan.diagnostic.Severity_1_0):
            self._severity = x
        else:
            raise ValueError(f'severity: expected uavcan.diagnostic.Severity_1_0 got {type(x).__name__}')

    @property
    def text(self) -> _np_.ndarray:
        """
        saturated uint8[<=255] text
        DSDL does not support strings natively yet. To interpret this array as a string,
        use tobytes() to convert the NumPy array to bytes, and then decode() to convert bytes to string:
        .text.tobytes().decode()
        When assigning a string to this property, no manual conversion is necessary (it will happen automatically).
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._text

    @text.setter
    def text(self, x: _ty_.Union[_np_.ndarray, _ty_.List[int], bytes, bytearray, str]) -> None:
        x = x.encode() if isinstance(x, str) else x  # Implicit string encoding
        if isinstance(x, (bytes, bytearray)) and len(x) <= 255:
            # Fast zero-copy initialization from buffer. Necessary when dealing with images, point clouds, etc.
            # Mutability will be inherited; e.g., bytes - immutable, bytearray - mutable.
            self._text = _np_.frombuffer(x, _np_.uint8)
        elif isinstance(x, _np_.ndarray) and x.dtype == _np_.uint8 and x.ndim == 1 and x.size <= 255:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._text = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.uint8).flatten()
            if not x.size <= 255:  # Length cannot be checked before casting and flattening
                raise ValueError(f'text: invalid array length: not {x.size} <= 255')
            self._text = x
        assert isinstance(self._text, _np_.ndarray)
        assert self._text.dtype == _np_.uint8
        assert self._text.ndim == 1
        assert len(self._text) <= 255

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Record_1_1._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.timestamp._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        _ser_.pad_to_alignment(8)
        self.severity._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        # Variable-length array: length field byte-aligned: True; all elements byte-aligned: True.
        assert len(self.text) <= 255, 'self.text: saturated uint8[<=255]'
        _ser_.add_aligned_u8(len(self.text))
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.text)
        _ser_.pad_to_alignment(8)
        assert 72 <= (_ser_.current_bit_length - _base_offset_) <= 2112, \
            'Bad serialization of uavcan.diagnostic.Record.1.1'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Record_1_1._DeserializerTypeVar_) -> Record_1_1:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "timestamp"
        _des_.pad_to_alignment(8)
        _f0_ = uavcan.time.SynchronizedTimestamp_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "severity"
        _des_.pad_to_alignment(8)
        _f1_ = uavcan.diagnostic.Severity_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f2_ holds the value of "text"
        # Length field byte-aligned: True; all elements byte-aligned: True.
        _len0_ = _des_.fetch_aligned_u8()
        assert _len0_ >= 0
        if _len0_ > 255:
            raise _des_.FormatError(f'Variable array length prefix {_len0_} > 255')
        _f2_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.uint8, _len0_)
        assert len(_f2_) <= 255, 'saturated uint8[<=255]'
        self = Record_1_1(
            timestamp=_f0_,
            severity=_f1_,
            text=_f2_)
        _des_.pad_to_alignment(8)
        assert 72 <= (_des_.consumed_bit_length - _base_offset_) <= 2112, \
            'Bad deserialization of uavcan.diagnostic.Record.1.1'
        assert isinstance(self, Record_1_1)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'timestamp=%s' % self.timestamp,
            'severity=%s' % self.severity,
            'text=%s' % repr(bytes(self.text))[1:],
        ])
        return f'uavcan.diagnostic.Record.1.1({_o_0_})'

    _FIXED_PORT_ID_ = 8184
    _EXTENT_BYTES_ = 300

    _MODEL_: _pydsdl_.DelimitedType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{^vH+ix958Mo^s9-my=B+aEQAyZmXo7(Hd&Be47;<`x_Ha;ni(?%6=x@ULn8E0?o?Aks-73~8kkyh%8Zl%5;c&w1%'
        'x&Hv7h$kKpm3ZR;RY*MWmItKreY4-5b9~DMwUM&loVkAAH{b0yes{-*L&pZpzx;UI@wDe#EiDq|`0AF^_J!4Qqacp7N=2FPeO34>'
        'fTp+5iADKAIrd)pPC1(IYN;?3Nht^Nz1PwtbJHvl>!<8&g-!rl9L<~+*9k38IZI)rQ{`Io!i^HI%voziBw9rw?lb%bwLd8BL3{8Q'
        '<$GnmyXB;5qS{$1bonFLbQ_Mlv&wwuMJ0T%$3~;&IjPf1kvBP9b;?HmG;x)xKv>s0p(~RpRJTA*=+LPX#HHLL_W>sZ$cfw!r^`dM'
        '{OERk#0e@(tpFbfuZLPKg~GcWreaAX>y@*+)mCZC7vWMWOM4o)bRC_xg2)3dpUw}zUT=iUtXUYF!y#17&&&BTf4l`ehMtpn{TtoM'
        '+92BQK)FezLB}EJct^{N-15f19vK)|kb;L<&=v`g7J1(+%~R>5TskX)$Bx#*<64ET;5rHfcM>=vagq)X;Afa}6~cToGqoDHDfPpq'
        'QKFV$cvM-!8aK00!MyEgF~*hVo>)|%6CR6X!ii&FxlRgqZgJek&5{K7=`O*OGA$Z#QM@g9B7Ty=-N5q2Bno=F>+bcL&3FKeiDaB>'
        'A<QH&wnXR{1XbY@^d>6`WHYQNb9w`$0OnR4KNHAh8u3u9pqk*b=trv+f8FsjXD2`<d{ueCr*IwM@x?}i^9ern<1=U1YZj(E?I=t6'
        ')YSAD-Vsis$N8#MuEe1jZZ7Rue1@MrZT9S23w&o_I|*NnGT(!P-~`Sy@H<y%?Ig<YR4jlYaFyyVx1csy2HfI}oPkqQ8D$!0nd4#D'
        '%U}!cz-h3tSW}>{Fa<m2Zlbi(Rwc}=54ND(iP@PZ9}T0FUwn0pgC&HZ%LLAIodk>`i&0<ac)J5miYLZS$B!Iy$8b>)11!V%LVZ;{'
        'K=zklvX+kT;|-&^E%{=?Os|eu6g@=+0y-)iO}qC1M)6#VW`R0La5RLA;h;oqmEZ^mb2b}==q72`@8nVW47E<!)ABhvW)Gl0$??i{'
        'hOam6=G8ZwrL^)BZ;2$@c(k!MxHr_s%`jRGtrB9PVW`ZH)j>h5#b9t4%+`ejHgD|H@oRqMi}?tM>|(Em@r%@k@qF-PiJa+n))x7}'
        'zBt%wcdE#WQcTF>a#~Jh5Kue;hk`o^ue_7*Yb~lZ;kEFhTFNV%`TmxUvcwfI;EPu5K)A@|WE#Yi9p`42P9WzKw}SBW)XGVJGS1rI'
        'o2^7FWj=1%3!-|Wa<9oMfKH-DCbtZr)+y_xRn3BM*piNhW6{A|<bvfLQ1hRgl}qCR91lQy01uB6@OM-rS|+%y11_1aM#;?yWAnQ2'
        'L~|?VNU()euJa+-Ao8=y%Z-!w&Ve6NElKbq&|4Hh2=nM*w8(Y@J3;)Z<E-(r6_^tx6FL^IT2y_O3@PBIurS)TeYnXJwI%d|GYFk-'
        '{9WdIUQy{4^ZT0UnrS}NisCZo+ijvdK|6x$0j<u7Afm8$75vRfqohAcyAm9{l-Kh|Uw1r=ew!xAw{WzX`91{rjid6#_sdaxy3lP%'
        ')p4~$X|t>iat12I#03p!4I9Ilyues+Q+p8C4HWhxM2C<*QrJ7__fDjPg}saVhpC?t9ijdP(p`nUo96F9$_jfg(jA4pkLEv$ba!Dt'
        'M&tXD?kwyBw9i4L2MYUfq>mN$A*A~X`!Lcyg?$8Rqp*+C`X}hzC+VE0XrHgqdB>1GRoGug`eb1rNBTrzbEHQL`)Q;{3i}&K4;S_`'
        'NDmeEvq&E=>~A7HSlB0suji2NFYHm`Zw%?9h5aq!^LeCu3wxaSogjHF;(HS5NMWBO{!bwtF6=3i;|0>kX_Ds*(xJjWOLCnf{Z5m7'
        '->&Z6ru(;FBKjSoFBAPP(eDvGPxKPe8$>11HKMnPenj+RqMs1`l;~$fKPP&(qH}DJ8b|BKXx*5u8<*<Fjk+Q0##-IDT{k|e8z0w='
        'PwK{}b>p+T@p;|2ON|WbH;DO=DKL0bUmHU=<dl)LS5aE|udl{c4(JP7R8Q6MZBuB2U<V;Gc!}S_jHDK!2B12sD!+O=QD%(7717aV'
        'Q?Ujqr7qA`rKpaA$O?%8wudSQ3$7@-38jeR3X?gzWo}=+{N&~;{u-7@D(&2>Q0_~&Ly&II)rodzl`^Gu<MY9)Fx9jh_o3l)C;^r*'
        '?3+sOq^U5l8W4%#SmBuEx|boabE3P&XcnpfC4}5R)(z6*7{VJE@;5KX-oEu)thTt37cMRcA?Sw6)h1V@n|Oz8kcdWI>9&QbADd9V'
        'n*r{4D+)6lhy=&@qAH!UG=>@xax<h>lsgbE6f{Z)$hHq#U?=3I#8jtR_`*#acs9gg6#!RV9*`*kB?n$_&HPKfOa%p6#WL<7s<ejE'
        'LkYD}j8*0P4JfcoF`%XJj0V?j1&sAC#1&YQ=`1!C5bQtdDGh}pq}DNGT&M198VmC?vlq};R_4|*4f(oz5Fr9nDnucqa4$1z^N{l>'
        'Mx7ep=unM`^;$h2+|2<^14_ijCgoKgS-F`7X-~dP`A@#mUx+;b^RHfb<@#&Lyx(Qs6pzTTqs-xH5`jX6mQjS2jn&v*OjI|iSP}@}'
        'picyw(C#3HaWX&M#PX?!V0p*o=EbYXar&AFje)BWY$&L;vf;XU?Hdp*z5>pt9)j~-&8rKSD^tnt&%1H_ua@~29)kJdH)rOXmz%~`'
        'e%fWF3e2Y7ZHFj`57+?%2XM6NBq5GqU2AZwzMl-WUw4HN;eBN|{V>*kVSfJVys@1vB#4s;4ht&gMUp^V`f6D}^AN1F+4;+0JTq6e'
        '(?34!0BT+@1;As-e2A0(e?c67)q&(p@@x{~?8E4P=E{Zn1(e{OCd86OdQCB$c#uG$TmT7NmAF};jnz{$@<d=B4FL2&LQjFI)Vu&7'
        'O4?qW2bSSn54y^W$oF66U*zBA-{e2#KjeSpzvX}B-Q{6O{L4f5Ie?#i_&J83C-5_hpJ(Bd$xC<S<)-|8?tBSowO77O*5yk-OqEv<'
        'l8%~S(t~$B4Ri~J>eZ^0P5FaL?gjZ~7f}7M+j_eXMhyXsk{+TbDQqSe;s4SDW2K=DSZQzrR$_#e7-1#00V^@WN{p})+kllAVI@Xb'
        'i4j&}gq0X!B}Q0@ZNN&5uo5Gz#0V=f!b*&=5+kg{2rDtdN{p})Bdo*-D>1@KjIa_Tti%W_F~UlWuo5Gz#0V=f!b*&=5+kg{Hee-2'
        'Scwr<VuY0#VI@Xbi4j&}gq0X!B}Q0@5msV^l^9_qMp%gvR$_#eSdqy;P@@J6Om_=wD<4=_kmpZr^ZuPAPN&R|yx~AE^i)p@GuXTS'
        '-Fa_IR23&Zi1z{us{+ey0QVy;*NGh$Ik3OT57ciDrexZ3-ScMM*3NJ}KQtSK_%0Q0`AmVQ;VVTVLVV$0=Q0dkrhls=^BC3UMJ!Ua'
        '-J8eF>P6y<4ep0~8P^+-i*t8}*ZUs%65K@-VwNTkof}~Hm`1m?BNb~Y-jt-k$+5#~G)?yQJLCP&opt=YDdLnnrYA9tIMQ0d#f@`e'
        '9+z+>KHF;1EnRA>z$%);>L2Cd<#!-P%0Dgt7USj5y76-E?s15i-j^FOr%z3vroY`l&^)z1Xx^@arpzF>OeDhb&=QR{x`7n2i61Q)'
        'WQPd|iYkDe9aAl22`B+@R)b18RGmuul-7kIoE~GbMAIo`XchHf%l(6Lw{Q8EpfB@d`9o--^?e!hZ*-&lG(`DnG$CU!%co&cWnAZB'
        ';Cy!g<_~6@yO-bZ&c6i4c%Jnys1DfBUzw!b4S@Wy3Wy&D(?F|uFoRkC9gg93F8>}{`EUy^4}wKG_x4DBxaHB`0+W`6+Xb>Q7Vvw='
        'f-Usd@1cC1w=e&yo;<qz8)(jr58lh8-yT6N)E=t)9GS!DyIYLnV(Wh)Bq>M^9RL6'
    )
    assert isinstance(_MODEL_, _pydsdl_.DelimitedType)
