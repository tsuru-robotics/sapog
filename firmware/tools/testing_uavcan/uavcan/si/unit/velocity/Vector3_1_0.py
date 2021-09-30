# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/si/unit/velocity/Vector3.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.487034 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.unit.velocity.Vector3
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class Vector3_1_0(_dsdl_.CompositeObject):
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
                 meter_per_second: _ty_.Optional[_ty_.Union[_np_.ndarray, _ty_.List[float]]] = None) -> None:
        """
        uavcan.si.unit.velocity.Vector3.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param meter_per_second: saturated float32[3] meter_per_second
        """
        self._meter_per_second: _np_.ndarray

        if meter_per_second is None:
            self.meter_per_second = _np_.zeros(3, _np_.float32)
        else:
            if isinstance(meter_per_second, _np_.ndarray) and meter_per_second.dtype == _np_.float32 and meter_per_second.ndim == 1 and meter_per_second.size == 3:
                # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
                self._meter_per_second = meter_per_second
            else:
                # Last resort, slow construction of a new array. New memory may be allocated.
                meter_per_second = _np_.array(meter_per_second, _np_.float32).flatten()
                if not meter_per_second.size == 3:  # Length cannot be checked before casting and flattening
                    raise ValueError(f'meter_per_second: invalid array length: not {meter_per_second.size} == 3')
                self._meter_per_second = meter_per_second
            assert isinstance(self._meter_per_second, _np_.ndarray)
            assert self._meter_per_second.dtype == _np_.float32
            assert self._meter_per_second.ndim == 1
            assert len(self._meter_per_second) == 3

    @property
    def meter_per_second(self) -> _np_.ndarray:
        """
        saturated float32[3] meter_per_second
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._meter_per_second

    @meter_per_second.setter
    def meter_per_second(self, x: _ty_.Union[_np_.ndarray, _ty_.List[float]]) -> None:
        if isinstance(x, _np_.ndarray) and x.dtype == _np_.float32 and x.ndim == 1 and x.size == 3:
            # Fast binding if the source array has the same type and dimensionality. Beware of the shared reference.
            self._meter_per_second = x
        else:
            # Last resort, slow construction of a new array. New memory may be allocated.
            x = _np_.array(x, _np_.float32).flatten()
            if not x.size == 3:  # Length cannot be checked before casting and flattening
                raise ValueError(f'meter_per_second: invalid array length: not {x.size} == 3')
            self._meter_per_second = x
        assert isinstance(self._meter_per_second, _np_.ndarray)
        assert self._meter_per_second.dtype == _np_.float32
        assert self._meter_per_second.ndim == 1
        assert len(self._meter_per_second) == 3

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Vector3_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        assert len(self.meter_per_second) == 3, 'self.meter_per_second: saturated float32[3]'
        _ser_.add_aligned_array_of_standard_bit_length_primitives(self.meter_per_second)
        _ser_.pad_to_alignment(8)
        assert 96 <= (_ser_.current_bit_length - _base_offset_) <= 96, \
            'Bad serialization of uavcan.si.unit.velocity.Vector3.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Vector3_1_0._DeserializerTypeVar_) -> Vector3_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "meter_per_second"
        _f0_ = _des_.fetch_aligned_array_of_standard_bit_length_primitives(_np_.float32, 3)
        assert len(_f0_) == 3, 'saturated float32[3]'
        self = Vector3_1_0(
            meter_per_second=_f0_)
        _des_.pad_to_alignment(8)
        assert 96 <= (_des_.consumed_bit_length - _base_offset_) <= 96, \
            'Bad deserialization of uavcan.si.unit.velocity.Vector3.1.0'
        assert isinstance(self, Vector3_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'meter_per_second=%s' % _np_.array2string(self.meter_per_second, separator=',', edgeitems=10, threshold=1024, max_line_width=10240000),
        ])
        return f'uavcan.si.unit.velocity.Vector3.1.0({_o_0_})'

    _EXTENT_BYTES_ = 12

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{?YX-%k`V5I*D(5K$51gFe8M;sd+)V-F7B)Z{c-I0+cuOzCdRwW0eXZTG^GkjR5Zk|vT+|6iwfhX?3wvPru$^UXKk'
        '%<Q-7Z&R%d9<!2{L=oX3MJ30ApW;YR55-xMXNqfT&Eme6MXU=+zmz$(SN6@hJ+o_O2BkOw`$~cPF-|?jy&~n>>r;`%T$kPfjddoQ'
        '*36+km5OJnWfe1fFgjn^a4M|)u;<n+Ags0IQK6}_U+pAPf1RwE>2NB@n9Ku2u*OI`hUVpja4B(V&9e?ap=6t;J<Z;^Pq)ijL{!j('
        'rg{W6flDrV!Zq)M$9zX*Sl>ojKoQqS43gMz75K$iX_RDyTK2*`-@OiZVcrL@?Kl%?Qu%K8fFx2HrvyuK6X+-4B)A7E7sMq#k~r3&'
        'r2>sRqcdQb*Ug~TXg8X{#zwQ<YP8#}t#-Y>SqtjzX3!2=^^L7YD+p@V<tidG5A1U6nr6dkQ$>*g#8=maj|qSV`tIGDhwr%_%DE5M'
        'kpyNMWw|x0lR#9NM48~RHOo6R$v{>|{&P+xhM^e?c^}1$L#J8GJl&%?)%^c{_s}tLXK%spakmfx%kr)hVD+&msQqQv!qrO^LFHAH'
        '@YIHf?to9+Vb(RN5Euf&Dd$<aR3JM&$#FWE+inrLP&Q+pBvez0APv+MXDP7&Lo%qT0;*!Od}FLpR1Wv$%(88^q+mh_%_WVoro>*D'
        'N9f3nCCW3Y5hu25mXOK{8B;I_igFD7H%Gosa=*mKg<f~MuAe4p(CF8MpBE9Ri6rd-cYqx4gIZ5uyr}etd+IChyFK-<_tYQlsaN-E'
        '-p~h{f*4kiRJuig$?x-++6%VBy3Awsft)O0n?v!3s_$Y#c-s4?HDGPSFCZV9Z8!(ob;3jT5#CP#6OIJ+{s7_7`aG8e000'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)
