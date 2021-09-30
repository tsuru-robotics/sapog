# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/si/unit/velocity/Scalar.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.524252 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.unit.velocity.Scalar
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
                 meter_per_second: _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        uavcan.si.unit.velocity.Scalar.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param meter_per_second: saturated float32 meter_per_second
        """
        self._meter_per_second: float

        self.meter_per_second = meter_per_second if meter_per_second is not None else 0.0

    @property
    def meter_per_second(self) -> float:
        """
        saturated float32 meter_per_second
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._meter_per_second

    @meter_per_second.setter
    def meter_per_second(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._meter_per_second = x
        else:
            raise ValueError(f'meter_per_second: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Scalar_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        if _np_.isfinite(self.meter_per_second):
            if self.meter_per_second > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.meter_per_second < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.meter_per_second)
        else:
            _ser_.add_aligned_f32(self.meter_per_second)
        _ser_.pad_to_alignment(8)
        assert 32 <= (_ser_.current_bit_length - _base_offset_) <= 32, \
            'Bad serialization of uavcan.si.unit.velocity.Scalar.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Scalar_1_0._DeserializerTypeVar_) -> Scalar_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "meter_per_second"
        _f0_ = _des_.fetch_aligned_f32()
        self = Scalar_1_0(
            meter_per_second=_f0_)
        _des_.pad_to_alignment(8)
        assert 32 <= (_des_.consumed_bit_length - _base_offset_) <= 32, \
            'Bad deserialization of uavcan.si.unit.velocity.Scalar.1.0'
        assert isinstance(self, Scalar_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'meter_per_second=%s' % self.meter_per_second,
        ])
        return f'uavcan.si.unit.velocity.Scalar.1.0({_o_0_})'

    _EXTENT_BYTES_ = 4

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{?YWOHUL*5MBcaf)9wqqjD0s%<L0~gBMM>tRNBN&2)OYo1IR2rYHSacZno&&`8pWCX~O?zhO1IxQJnrNvcxMufDIp'
        '%>Vj5*SP$`vwF-eR|&DgNUG!s&6P+9(`Bu#bOOSIBWFBw-iY_(TEGQtpTQ|?g#}X465~%j9Wq)aRwllZE*T1?nRMgih*3oige5W*'
        '#!6j5(FltlruGH&@AMnr;0(eFq0SkZdnYV>gxhxdn*?EDPYT6nyDSq<9VIR<cw2dGWGS5-V#d8arK$TD&I-w;BT7^QS3rLQTQX`L'
        'DK!^RtcNFuSLLxRd5y9C7(y70uka4SI<bycoEm<;(Rb`q(gEJZ^Emj}Q05T6#k1^9ZR`;?JKbhGYj?UkJDsf8&a&Qa)@r?Ic3WAe'
        'n{|7wo!xe?+igOe<?~`8td_zFLu&l3V7lTE<_XsfLIV?Mczo@sBp*-6I)!4hShEP0i`ocAo#1dD9+G1@5}ef9I3hV5gf(KdH%wqa'
        '2~typ5<aJeE=6jkLO#<I95PBRt@R*1mZtnfjYyr=%BDEc$!b6*!boeME6Iov1Fz!18CN!)rdXLq?W9-QNhjJ#T1hjRqyPdcsKr%`'
        's9dCWD4BrsVyoCj;JLz!KEEP<MgS(dn?8j5ucUi(=^vpxl|Yyyx`wcETN67jbB#c7lYLQYlvO0}EfPSTHZvjJC9IGr&LRts4k_n&'
        'iT{#{moa+a6@nb!jADl&RbIdk*y?Zmv^l<@deR8`OFl=qrL3Yx(V(MfEJmH;bz}815u=(`myhhg=Qj6w@&~)WKkM=X000'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)
