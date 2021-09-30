# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/si/sample/length/Scalar.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.579864 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.sample.length.Scalar
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import uavcan.time


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Scalar_1_0(_dsdl_.CompositeObject):
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
                 meter:     _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        uavcan.si.sample.length.Scalar.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param timestamp: uavcan.time.SynchronizedTimestamp.1.0 timestamp
        :param meter:     saturated float32 meter
        """
        self._timestamp: uavcan.time.SynchronizedTimestamp_1_0
        self._meter:     float

        if timestamp is None:
            self.timestamp = uavcan.time.SynchronizedTimestamp_1_0()
        elif isinstance(timestamp, uavcan.time.SynchronizedTimestamp_1_0):
            self.timestamp = timestamp
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 '
                             f'got {type(timestamp).__name__}')

        self.meter = meter if meter is not None else 0.0

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
    def meter(self) -> float:
        """
        saturated float32 meter
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._meter

    @meter.setter
    def meter(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._meter = x
        else:
            raise ValueError(f'meter: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Scalar_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.timestamp._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        if _np_.isfinite(self.meter):
            if self.meter > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.meter < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.meter)
        else:
            _ser_.add_aligned_f32(self.meter)
        _ser_.pad_to_alignment(8)
        assert 88 <= (_ser_.current_bit_length - _base_offset_) <= 88, \
            'Bad serialization of uavcan.si.sample.length.Scalar.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Scalar_1_0._DeserializerTypeVar_) -> Scalar_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "timestamp"
        _des_.pad_to_alignment(8)
        _f0_ = uavcan.time.SynchronizedTimestamp_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "meter"
        _f1_ = _des_.fetch_aligned_f32()
        self = Scalar_1_0(
            timestamp=_f0_,
            meter=_f1_)
        _des_.pad_to_alignment(8)
        assert 88 <= (_des_.consumed_bit_length - _base_offset_) <= 88, \
            'Bad deserialization of uavcan.si.sample.length.Scalar.1.0'
        assert isinstance(self, Scalar_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'timestamp=%s' % self.timestamp,
            'meter=%s' % self.meter,
        ])
        return f'uavcan.si.sample.length.Scalar.1.0({_o_0_})'

    _EXTENT_BYTES_ = 11

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{^X7TW=h<6_#wvy7?N}j^iW_?If1edS|88uDnj0wysh)0b|*)>_lkMPB}BwlJMM0a#mUc1)7Hz7BD~u$P~y=$WO>)'
        '(e@!gfj;La1pNhh>^U=>mE_oO5g>hM$is6E&z1V~iN9YzJyHGSZ>6I^2chF?t|SZPQ|5)-as4Dp6D<ud^V3^KWxmN2e>6&Y`FXkg'
        'S^1}ODW7s<7Qz12j17GjJ6bxLMJb#Pc|0(}+45P)RGH7XL$0(;;!;fH)1O%S^O8=|iNBVgmHE8Oj8W3d4A<rFK=ezD8grHT)LqHL'
        ';J}zUH(-Xj1}zlF>P0b?U$eFu8F6Q86#GIYv3$ydN3fs`m|KczG22)oPJwoD&K_TQnH{N;ku-7$b}T%OwH(Ae_$W4fz|~O~&AXm7'
        'Ztaee_Q6V@Y2!vo09L+{UwY68!eh<`?A^mHbj@GNhh=`j1smglso=1n{mg@_%}3H#iROM12W5W34HCcH{@<~QiAREyIEy^4NU}o?'
        'acN=%Geoc<Cn?jK2Sm%*=R_wFCrp6~#ngyI@EIE-W8kkijWdTr?K%ielpMhJl61Ipv*JPr6OU=WOr$0O-;v-Gl5*8zX&OqO8Hl+<'
        'P>i1`g>uG6P*bM)90ZDZoGAXs3}OSvcT^G`NY~@=Rl-OFhH-V1XwEApKLNQqg^S8~0IO;!;ck^FveG^Ww*cdYEX+7sX%Z6iA-W0v'
        '?1af~ZQppmx84GmkX;#oo!n<&<9l;+gtSQK_r3L_o&|R1C7B_ePQOP+oGE>i><Z}%+=8Nr&B!5l$a=SudFU+Iok8v>vYTXK0E$2Z'
        'Az2)ApKHyO3`eyIkO)K?J+>Cy2FJi!j7Sf(8j)lgxhnOr9b_PaFwh2q`JM!S#Rl@2_)2Q2o%%8xA>@MeTN`&a$x@sca`%H}0+|ql'
        'FBRzXnS!LqQuNm?;*Fq4QDe$RVZy2yL!h7&IF;d#noyAl%^v`>7Ay=g!kBJ@khd!KTEz}Oa8$%$q0Uh=jsqmcqQSI4A1K_7Aut4-'
        'sGSlD;Y>cWk;GUgW?Xk-L0q-eHQE=~#XEEY>q#uur8E6_lWyMsbh8x8`HkOjl{~My$~TA`dgDo)?8Z)+pL8pO%KXiyDe%1%5)PZ$'
        'k(My?u*y#sHui{KJ_}d&aaF_qT}#7$KDkn&W!lR;o-Z8ggRVEK`zzjJNn8<YqLo2I2{<T)a^gX`pPzAe<Q@-P43sN_ax*{g>LgP>'
        'hmDZCDT8*Ai?)f<_J}>nObab<J&odSXSfo!)69d~bQK?DA&NX`qPkU=SG#VYZS+X{g$>kMbyl333)-P8m<F|2;I1vfav$9MpUt|Y'
        'Q2{{(m=93liGq4ZH)3W&*)k|evzw?Vtt#jBA&pg3DwU86MjWXj5RimfUFB7gALxM(AqN7g2>g~r(82<%7&FpKKoazyrq5PYHUyqT'
        'wRFmTxg!r{GK_#H+`(?^g%HUbO(q;PXSlR^{=3Xi{Zg8btM4s7PSgCjo1|q<UM573A}@jPfLHJFD6wttKGYjCi8>fECtY7aftTVz'
        'e)a(iu={<FNj%2g%`Ak0JbHdt^!`>Z(SD&l7}aSlp`<gJ2ltF*jDrgZwui(t4lhU+6iO%Y+(bc-Sv-z-te_|C_Y~q}K~LKCX}dmS'
        'an`QSA)YMgyyZWII8)Hmh$jkq#`2#<oG<7(yMG>Ws-Uk}ISYud6!Ze(xq@CqJX6q1h^GqrD&ky0FWd94S-n@Rp4Y9MH>|!l5nnIp'
        'Rm3X=eGBomf)d2b1-*v&YC*3fUMlF@h!+d`4&sG^zKgg}&>PmSMa1(3U9$EqBc3hjkF1?PMm$~6o7Uczy{}{KZX?bXbj8}gia1@+'
        'j=jg4^+(s<r;6+Gg09<p-Ln4e+xy+F<4)hR_!EmiwfMfppIQ95#a~$b(Big5VR6smGmBqX{L<oA7QeRmjm2**eplnYnMq4rZiuCZ'
        '=r_cN4YA!2q9OJg;#os{(GXuY#8(aRbwhm95Z^Y$cb3TD{RTZBCIvQcyXIl*hM6*J4qlYY`2>!p@jDWpdb4+7SehfRLzqnjW>ZHj'
        'J_ErK8^ALq!-wJf`Qlo4rPJ@Mb=TL|`n^uS-@DykUA?u^UG1-R``zB^`t44y+pT9urG6^n(5*qW_!mqPaR=r9Q=Aw775~n}#=iJq'
        'Q~WCDKfoZ+vR%LO+jXyM*RTA;Q$YNBAMFqyiI404a$h_gx1mqR)Wbuq=_1T<9BT0kdt5$Sw>X$8`0v3BrELk9PJ%1`00W=FuLpYn'
        'u?Y*mJ=Eg}^f<1OX&acf513qRci&sa&^rGI(9iK4Ee!ww'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)
