# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /tmp/yakut-dsdl-zmn42v0l/public_regulated_data_types-master/uavcan/node/port/ID.1.0.uavcan
#
# Generated at:  2021-09-29 15:15:51.689265 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.node.port.ID
# Version:       1.0
#
# pylint: skip-file

from __future__ import annotations
import numpy as _np_
import typing as _ty_
import pydsdl as _pydsdl_
import pyuavcan.dsdl as _dsdl_
import uavcan.node.port


# noinspection PyUnresolvedReferences, PyPep8, PyPep8Naming, SpellCheckingInspection, DuplicatedCode
class ID_1_0(_dsdl_.CompositeObject):
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
    def __init__(self, *,
                 subject_id: _ty_.Optional[uavcan.node.port.SubjectID_1_0] = None,
                 service_id: _ty_.Optional[uavcan.node.port.ServiceID_1_0] = None) -> None:
        """
        uavcan.node.port.ID.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        If no parameters are provided, the first field will be default-initialized and selected.
        If one parameter is provided, it will be used to initialize and select the field under the same name.
        If more than one parameter is provided, a ValueError will be raised.
        :param subject_id: uavcan.node.port.SubjectID.1.0 subject_id
        :param service_id: uavcan.node.port.ServiceID.1.0 service_id
        """
        self._subject_id: _ty_.Optional[uavcan.node.port.SubjectID_1_0] = None
        self._service_id: _ty_.Optional[uavcan.node.port.ServiceID_1_0] = None
        _init_cnt_: int = 0

        if subject_id is not None:
            _init_cnt_ += 1
            self.subject_id = subject_id

        if service_id is not None:
            _init_cnt_ += 1
            self.service_id = service_id

        if _init_cnt_ == 0:
            self.subject_id = uavcan.node.port.SubjectID_1_0()  # Default initialization
        elif _init_cnt_ == 1:
            pass  # A value is already assigned, nothing to do
        else:
            raise ValueError(f'Union cannot hold values of more than one field')

    @property
    def subject_id(self) -> _ty_.Optional[uavcan.node.port.SubjectID_1_0]:
        """
        uavcan.node.port.SubjectID.1.0 subject_id
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._subject_id

    @subject_id.setter
    def subject_id(self, x: uavcan.node.port.SubjectID_1_0) -> None:
        if isinstance(x, uavcan.node.port.SubjectID_1_0):
            self._subject_id = x
        else:
            raise ValueError(f'subject_id: expected uavcan.node.port.SubjectID_1_0 got {type(x).__name__}')
        self._service_id = None

    @property
    def service_id(self) -> _ty_.Optional[uavcan.node.port.ServiceID_1_0]:
        """
        uavcan.node.port.ServiceID.1.0 service_id
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._service_id

    @service_id.setter
    def service_id(self, x: uavcan.node.port.ServiceID_1_0) -> None:
        if isinstance(x, uavcan.node.port.ServiceID_1_0):
            self._service_id = x
        else:
            raise ValueError(f'service_id: expected uavcan.node.port.ServiceID_1_0 got {type(x).__name__}')
        self._subject_id = None

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: ID_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        if self.subject_id is not None:  # Union tag 0
            _ser_.add_aligned_u8(0)
            _ser_.pad_to_alignment(8)
            self.subject_id._serialize_(_ser_)
            assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        elif self.service_id is not None:  # Union tag 1
            _ser_.add_aligned_u8(1)
            _ser_.pad_to_alignment(8)
            self.service_id._serialize_(_ser_)
            assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        else:
            raise RuntimeError('Malformed union uavcan.node.port.ID.1.0')
        _ser_.pad_to_alignment(8)
        assert 24 <= (_ser_.current_bit_length - _base_offset_) <= 24, \
            'Bad serialization of uavcan.node.port.ID.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: ID_1_0._DeserializerTypeVar_) -> ID_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        _tag0_ = _des_.fetch_aligned_u8()
        if _tag0_ == 0:
            _des_.pad_to_alignment(8)
            _uni0_ = uavcan.node.port.SubjectID_1_0._deserialize_(_des_)
            assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
            self = ID_1_0(subject_id=_uni0_)
        elif _tag0_ == 1:
            _des_.pad_to_alignment(8)
            _uni1_ = uavcan.node.port.ServiceID_1_0._deserialize_(_des_)
            assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
            self = ID_1_0(service_id=_uni1_)
        else:
            raise _des_.FormatError(f'uavcan.node.port.ID.1.0: Union tag value {_tag0_} is invalid')
        _des_.pad_to_alignment(8)
        assert 24 <= (_des_.consumed_bit_length - _base_offset_) <= 24, \
            'Bad deserialization of uavcan.node.port.ID.1.0'
        assert isinstance(self, ID_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = '(MALFORMED UNION)'
        if self.subject_id is not None:
            _o_0_ = 'subject_id=%s' % self.subject_id
        if self.service_id is not None:
            _o_0_ = 'service_id=%s' % self.service_id
        return f'uavcan.node.port.ID.1.0({_o_0_})'

    _EXTENT_BYTES_ = 3

    _MODEL_: _pydsdl_.UnionType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8CxcXB0{`uo+m94Q6o+To+st0r#RWv<(hA}(ustj+0*Z=2h@@q?6GNh9b$9KYf}ZY9clFAUn8<_1O)7B`%157wzL@x+55D`C'
        'd20I1WtUq_cw~~vSJzXgs?P6B&G#d}{4rJOeDwab73N{&vRq`6NAe-}BjK_jX{Jdol`y(?JC;d&tCb4#*epCU-<f$m%3|KczPW<0'
        '1w3}+BouC%WXipK(da5$6IqUv3{>>^9V$OI-jG-M(L6GGl5wRn=@&}m<}0-K94~sKj2^utMHKcum|!7SoGI%Tt}=a7WksNhOl)uz'
        'M)mHeT)bKM_e7x3Qy7O@*D07nM_`ub%{|YhG?PuK<eJ_5?Kqc>ScI2jB^n~zctn%Tmx@IqZYVI`G&&scT(Ks)VPK!$d97>6PIE6{'
        '-xb@1r&RgD+%S4O%N379o`r*k)(ao^G`hy40zDXEVG<Z!G1$6QS1%;7oum5Op96<V2fS%G2=lN|S{T0a*_Q^6z)?NM$k^WQhQ)(4'
        '6S=*!4co2W;0oJ#)HM&wy0)6}z_#Yte~HT2uSZTVomnz=Be`GrLeCA{IP+U&_*lOV!yY&R^#ac;6u54{l?ctc-pW?x0}(QNV@!r-'
        'MQ>wyQe=U^j!3YS<7sGKSIxBE;`a-+Xq{ht*o>EtuN{l(Y2imQV3}wXku}*5mwd5_hb^*t85ngN7<Ic$y%!knl6%Z8yYZSC@Eq66'
        'M67HutjR!_bvU9=)A&W4;M@Y?WIS$&+`*AfC{`s#hU2#!g*|yH0=X)K&I!8q;`|7Y>`?c}`!|d$sLgewr_M|DMW=pK^sZMAvm`az'
        'd7hEH)$|iQ1l+<E(M&Lc?dn%kk#Ut|{YV{S0Z7yqT-7tzco@pK@zfx=WqVhODB@Xbb1y9aZ05b`cJ8C})6#<Rs)djHY|7Ypv$nt='
        '*uuC~0A7hT>J8a>mA1EqIBYr8_C}~aO7$_zk+wH(xuxw@slR49-u5Oe$J*Yc<!IZRqVdy~!)<RX&6^>6vowF3<!sw~gE&XrPTWD<'
        'Nqm#Ii})6CH}P%a9^zi&KH`3&Lwtw$F7W{IAn`roA>#YQdEx@`F!2cSC~=YK66?fc#3kZ!;tAq1@g(sB;wj>3;u+$H#E*z)i60X`'
        'A%03cSF*sQh{=Y>o!<v)^KHVw3^kFL>ayaui3%Hg$r*OMD7}{weQ|mp$cweXyhxdq7Ia@Wyq88{8BUQF;H(}#xipac;GCWL7yJqT'
        'z~2R&Uxy1TaPd{=uI{b}a~E7H^HkaQ|ML`l4qmyd6}a9@1b2F+y94sCq5R=%t9oGGEPR7s{#xU&H4aan5_TDmePNSAeuHiICWk5&'
        '_`NTZyRTFv&r-*)w{whtl{lGL6`3O>>L9aq?vQSrq+2gDk~?8V6hM-T*ipRU$Pk|fC>zw2714behfcEEDcfa_+EU!9#zhlflL3#M'
        '%NI9KvqPP4ad{c{%-~aDhT#(U=E2u5y>|P#sEWDhkT+yA4J`bGr~4AUULW`|-+`}1``C(~`6|%0@=<_~9{WJwp!BL$`k<-l&Oe0B'
        'Chj?Smv-(A_*di`vI0C=!CUXN?ZUQQy|!Kg+1P9&$Ndj{cG^w03;+N'
    )
    assert isinstance(_MODEL_, _pydsdl_.UnionType)
