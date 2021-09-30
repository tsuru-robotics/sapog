# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/si/unit/power/Scalar.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.504689 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.unit.power.Scalar
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


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
                 watt: _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        uavcan.si.unit.power.Scalar.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param watt: saturated float32 watt
        """
        self._watt: float

        self.watt = watt if watt is not None else 0.0

    @property
    def watt(self) -> float:
        """
        saturated float32 watt
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._watt

    @watt.setter
    def watt(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._watt = x
        else:
            raise ValueError(f'watt: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Scalar_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        if _np_.isfinite(self.watt):
            if self.watt > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.watt < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.watt)
        else:
            _ser_.add_aligned_f32(self.watt)
        _ser_.pad_to_alignment(8)
        assert 32 <= (_ser_.current_bit_length - _base_offset_) <= 32, \
            'Bad serialization of uavcan.si.unit.power.Scalar.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Scalar_1_0._DeserializerTypeVar_) -> Scalar_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "watt"
        _f0_ = _des_.fetch_aligned_f32()
        self = Scalar_1_0(
            watt=_f0_)
        _des_.pad_to_alignment(8)
        assert 32 <= (_des_.consumed_bit_length - _base_offset_) <= 32, \
            'Bad deserialization of uavcan.si.unit.power.Scalar.1.0'
        assert isinstance(self, Scalar_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'watt=%s' % self.watt,
        ])
        return f'uavcan.si.unit.power.Scalar.1.0({_o_0_})'

    _EXTENT_BYTES_ = 4

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{?YWO-~d-5M2W(f*&CgFCOG1aA0OXW^p)p(S*wi5;5LPr+d0#I`+(T`eR{9NaUcAq!Udj|Bk=S>RoUV!<?$8s$SQ7'
        '_4>=~uirDR@fV)!5w~0=#0n#+k|&fYk&vRPbYrCx5FYM3;|u4F_%PA}E@1r(PGK#~k(ySRf9C11pmkzp;%n&=-5d#%>=#r~17V&F'
        'g|V`!p=^bFA1~tz7~C1OzQGxUMM9l3l6faAe1h8s`db8HZd(e)r-LjIP8}sKPIp_oHnNgV4zc3?wrZ&Rm&+ny(h()<Ls!CJ1tAM+'
        '9jO{Fpj-}5_paJwTk-~TJ28bcT3_Kkgk@qKtvNOPI?#8-spuh!;(5IIz|g`WeT%YeU&e?LR(n~yn|FKJ=4LPNck{fzm3KNX+gT^?'
        'WqH=`Y;JY?S=NSlmuKZ%m_0&0Aj}fp6cAeYlZGePgd}V<+0H4HtL2hKf?Q}L3hD%h^YDlq$Ya5YZj2+6!){n2w(+JAm{5XfisJ{C'
        'x=N=b`q{gUDC)*ZRcGB{Tcz4FB@1H2p;r-dx&gaUp*q5(6IY~GrqLDY*cIu-6-g&)CzCwj*d?`ip%Jx<OB>2Uz<Ie=t|L9BP^%YL'
        'E1gP<h3@7V!h_e+y&a$T@p!r1Fhd#*VdXXuJE~ZNWN?xlQ8j3oxR!TX80s1`wa8skloD-M=Hc-k<y_W>{}q+5Vs_UnBssd7MT8+$'
        'Uce7n8?5}a4Bv*H0Ks71Go)L|I=T-7dK`m$(SfLN>|P+^Skrp^e0Dvv%(LVVB6J)+$pZiY'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)
