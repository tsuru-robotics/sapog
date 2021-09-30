# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/reg/drone/physics/kinematics/translation/Velocity1VarTs.0.1.uavcan
#
# Generated at:  2021-09-29 15:15:52.650032 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     reg.drone.physics.kinematics.translation.Velocity1VarTs
# Version:       0.1
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import uavcan.si.sample.velocity


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Velocity1VarTs_0_1(_dsdl_.CompositeObject):
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
                 value:          _ty_.Optional[uavcan.si.sample.velocity.Scalar_1_0] = None,
                 error_variance: _ty_.Optional[_ty_.Union[int, float, _np_.float16]] = None) -> None:
        """
        reg.drone.physics.kinematics.translation.Velocity1VarTs.0.1
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param value:          uavcan.si.sample.velocity.Scalar.1.0 value
        :param error_variance: saturated float16 error_variance
        """
        self._value:          uavcan.si.sample.velocity.Scalar_1_0
        self._error_variance: float

        if value is None:
            self.value = uavcan.si.sample.velocity.Scalar_1_0()
        elif isinstance(value, uavcan.si.sample.velocity.Scalar_1_0):
            self.value = value
        else:
            raise ValueError(f'value: expected uavcan.si.sample.velocity.Scalar_1_0 '
                             f'got {type(value).__name__}')

        self.error_variance = error_variance if error_variance is not None else 0.0

    @property
    def value(self) -> uavcan.si.sample.velocity.Scalar_1_0:
        """
        uavcan.si.sample.velocity.Scalar.1.0 value
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._value

    @value.setter
    def value(self, x: uavcan.si.sample.velocity.Scalar_1_0) -> None:
        if isinstance(x, uavcan.si.sample.velocity.Scalar_1_0):
            self._value = x
        else:
            raise ValueError(f'value: expected uavcan.si.sample.velocity.Scalar_1_0 got {type(x).__name__}')

    @property
    def error_variance(self) -> float:
        """
        saturated float16 error_variance
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._error_variance

    @error_variance.setter
    def error_variance(self, x: _ty_.Union[int, float, _np_.float16]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -65504.0 <= x <= 65504.0
        if in_range or not _np_.isfinite(x):
            self._error_variance = x
        else:
            raise ValueError(f'error_variance: value {x} is not in [-65504, 65504]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Velocity1VarTs_0_1._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.value._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        if _np_.isfinite(self.error_variance):
            if self.error_variance > 65504.0:
                _ser_.add_aligned_f16(65504.0)
            elif self.error_variance < -65504.0:
                _ser_.add_aligned_f16(-65504.0)
            else:
                _ser_.add_aligned_f16(self.error_variance)
        else:
            _ser_.add_aligned_f16(self.error_variance)
        _ser_.pad_to_alignment(8)
        assert 104 <= (_ser_.current_bit_length - _base_offset_) <= 104, \
            'Bad serialization of reg.drone.physics.kinematics.translation.Velocity1VarTs.0.1'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Velocity1VarTs_0_1._DeserializerTypeVar_) -> Velocity1VarTs_0_1:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "value"
        _des_.pad_to_alignment(8)
        _f0_ = uavcan.si.sample.velocity.Scalar_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "error_variance"
        _f1_ = _des_.fetch_aligned_f16()
        self = Velocity1VarTs_0_1(
            value=_f0_,
            error_variance=_f1_)
        _des_.pad_to_alignment(8)
        assert 104 <= (_des_.consumed_bit_length - _base_offset_) <= 104, \
            'Bad deserialization of reg.drone.physics.kinematics.translation.Velocity1VarTs.0.1'
        assert isinstance(self, Velocity1VarTs_0_1)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'value=%s' % self.value,
            'error_variance=%s' % self.error_variance,
        ])
        return f'reg.drone.physics.kinematics.translation.Velocity1VarTs.0.1({_o_0_})'

    _EXTENT_BYTES_ = 13

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8D1%gC0{^X7-ESOM6}OW({>q0FCuy2edRszbm+Y+9*>yH41xkw5=q667-PB5zj_%A{@4aNcxOc|(Mk=BYpjaA-kvd5I6Z$9g'
        'Pl#wG1P`bZZ%9ZL&mi@I2hN$fv%5}XK!Qll@9f+&=bU@K=a)x*yEr#i{>xs9`=0iE%hp^;=F3OS@wsKYQ4mL3CcMawuO}*XlT`7I'
        'e$0!Hi^Y$M4~vCt!VXyg=hqbPS)PhQZpEUnrK_!nGUNeEkW3T{wGVU@TKBjgxiaau?lHBYi)_l?=1Rj!A;z-FdxrkFpks9W*TqLg'
        'HfysaQPN2hu8Rkt^8jlHTtzmqD!K0st(>tvmM}X()5W3cp_s@>%C=n=T3T9~1u+QOHpW@&F7ufx#H5&}<8%xS5ywEem@{wBkH~r1'
        '$Vp_tt@VEB3UGvc#Jvr8pc4@N?*tumpIFI2CUP6@GyiU=WiRC3tuWy|uJ*@Z)^=oK`#kI=qM%*4t;=*`2ayN2y_lVQyB376SvTSA'
        '4jzGv$A4A4Q)Fjsurc(Q@<s*ir4C$eHju80G<T!WE3zZD7rDje-wut9Z3s@nG;p{g(H0ru(j*ZqA%bml5;Lv2N3;xGPIMG-!W5`b'
        'O!Y|sKf{E`5co^Z#F{~&<~azBl<dLrg0#4GrQ|{f6NhQONTenn-+~nLNX%7(#j!8lD#HkhaZ{yG&fpc)lxjW$fg%nkivK)?*ud*s'
        'Dhh_u^&otuFcN@aTwNiW^ODJpK(3DAqB88kQ?)JOZlx)*)II~Z0OPiqpK`P^iAcz|(M|B*mLKg@_6^QED-Cc7*^wUD$z29E-k6yo'
        'q(PQH=&bDbEU+^tN)xiY-0hG)XG&ioJ3_hwk060VNL}&<S!tItN8SayQ^*}fcB0hxKoMvlBn?CEa;=$?e!nsS5`oA>53B{Z!E0bG'
        'Mx+B;6A`5vxk~kL?4=-rFwh2q`K|<ig$d*_ah23kTh(Q5`j89KZQOigjVy#wLRQ~gBxPTSBL(_grXVTO82xpPIDIH~)EKkAAF(pV'
        '5GZIhR%!S~9V!x_`8{CPg84p17}Kri^G3;Dso3H}M+F=nR5_Xq;s8l;Il;6*A1FKxAut4-sI3AD;Y2odGYYXxl0n@;3%F#cMcNgw'
        'iYs&s>q#`L(wTgBjjr8&Z><om?9zR%qNi1t`37-AZ#)d6ozN<>qjqUfk-b<q1-=_Y!eLX~*Ak}QDf5&0wLRkXY#OfY;!|v^tA>X2'
        'Y<#Ie%e0d^Jewcsr?%6t8aUo!NxULn6P*+qipN1IloR)gz3ha&C3m@JW1wv56>HfkTSuvKIUM-hjv2IzOf-`qZuZ&3G-;sajYmP)'
        'Ufy2vn{nzuZQ3v)QXfSQo3U<G<<+bjXcIlsd}af+TGo<PaX~w@1=FAw3*0s(SnPqDKVPd#8Wj*!fcXFw9x14IbR%Xalr4jjOm-sm'
        'uu<l`9?@7vrBn&IkcfRX1Og&It*X2%@}VC1A!JWL6@lNP09u%56k|p@5lDjmQ}@}j%C><gQVkt*S8mCXOokEgkXzVo9Umfjsm_F9'
        'bB0SNPya5mV?UP3?eh0JAEaq^*pA{NBL@l5{lJMJJmA$kJcvx&y9@Qkl1L4Q%u(AFP~e5w%uc?|JnVkoU=k1TbS?E^boQS<6|euM'
        'SfJfpJ23L&N<u-WQU~rC$Pfn?5NsETNgQ5~EGU$Y<9lN{J!J4O;-Q=#F~27e$8&nrJfAerrwmS;=QD^$b2@AIk0DOw^f=;?oSrcJ'
        'ClP0JI%m#LAx`A<w2?E9csi$N5a)7w7V$(*&mkVm>2ruPIX!RQf8OZ5VD!9T<b2EMdlB)4oPHbeLQY>od_JcH@qA8SMtm-(uOObw'
        '>30y%=JX=snVfzXaXzP)j9r%zPvvyM*tdvyGN-Q^JHLl`Jf~NTy$y3;%h=sSoX+WzvA=~lnbT!+kE_NXZF8Rv;^CaGn0s9_{_UFk'
        'U9aL!Zy0>d;P(xhyr4fY_(Ov~GWeFkO@qSVuEEC!KQZ{J!OsjnG5DpyuMB=&;hm{*L!7UPg_`Kr#9KA7Sreirc5C8sO?*-lpVq`@'
        'HSwe-zO0F_YT|1{q_Dq1&xc8Y&D%V4uyw;snNEfqWh)!Q(KK90FJ{xLFf5aO+ab&*0<-CcXg&tP0qen<lHy|clkD=<_R?~9`D%M*'
        '<!ZOH-0gO*cU!G%OYK(oYP;L+v{tS!ciQc0c9iPp0uJ5UhRU|hN+??5a~LY(7OMK4xFG%{zDNb#6SvpIovinNm<d`otL3~|FXzo_'
        'IUgMf;_e<=B7Q11s%G<^xIgGg_JF!S(x=YCK*tFeKC|Iv(^bEN5rf|x&y@DQ=+SZTi-74b;qPZ37Io9n;>jAExFem9K<DEcxi^7('
        '^BLSd?1l%Qn-rL+7KF<2Bhml;Al`E(-r|oC<cXC|XQ@35;R&u(q+rW{PYu}0F^x{Yzfi`tS;chmgXIUsAf|s8r^G+SKZY^=#s3mh'
        'IBS+)iB0pB*c^T(Hb=e^oBO{KA<(UTq0atr8{T7z)HzWN>*4HX<;q*%(we#J;GV$i<x5t(Gz{eGs}{CZojT<tho$pBeHNCPH?s=E'
        '9TtfwYz)-G$Ol5geRydQuIfW8%2fatKgD*)`mJhl@FXk@iQl)1|2}#DQnCH@pv3(1ATbB2^v!&n8|0$^CNX5H({TS|%s%U1{}ryn'
        'G!Os)'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)
