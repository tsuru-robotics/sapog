# AUTOGENERATED, DO NOT EDIT.
#
# Source file:
# /home/silver/zubax/sapog/firmware/tools/testing_uavcan/public_regulated_data_types/uavcan/si/sample/volume/Scalar.1.0.uavcan
#
# Generated at:  2021-09-29 15:16:17.630705 UTC
# Is deprecated: no
# Fixed port ID: None
# Full name:     uavcan.si.sample.volume.Scalar
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
                 timestamp:   _ty_.Optional[uavcan.time.SynchronizedTimestamp_1_0] = None,
                 cubic_meter: _ty_.Optional[_ty_.Union[int, float, _np_.float32]] = None) -> None:
        """
        uavcan.si.sample.volume.Scalar.1.0
        Raises ValueError if any of the primitive values are outside the permitted range, regardless of the cast mode.
        :param timestamp:   uavcan.time.SynchronizedTimestamp.1.0 timestamp
        :param cubic_meter: saturated float32 cubic_meter
        """
        self._timestamp:   uavcan.time.SynchronizedTimestamp_1_0
        self._cubic_meter: float

        if timestamp is None:
            self.timestamp = uavcan.time.SynchronizedTimestamp_1_0()
        elif isinstance(timestamp, uavcan.time.SynchronizedTimestamp_1_0):
            self.timestamp = timestamp
        else:
            raise ValueError(f'timestamp: expected uavcan.time.SynchronizedTimestamp_1_0 '
                             f'got {type(timestamp).__name__}')

        self.cubic_meter = cubic_meter if cubic_meter is not None else 0.0

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
    def cubic_meter(self) -> float:
        """
        saturated float32 cubic_meter
        The setter raises ValueError if the supplied value exceeds the valid range or otherwise inapplicable.
        """
        return self._cubic_meter

    @cubic_meter.setter
    def cubic_meter(self, x: _ty_.Union[int, float, _np_.float32]) -> None:
        """Raises ValueError if the value is finite and outside of the permitted range, regardless of the cast mode."""
        x = float(x)
        in_range = -340282346638528859811704183484516925440.0 <= x <= 340282346638528859811704183484516925440.0
        if in_range or not _np_.isfinite(x):
            self._cubic_meter = x
        else:
            raise ValueError(f'cubic_meter: value {x} is not in [-340282346638528859811704183484516925440, 340282346638528859811704183484516925440]')

    # noinspection PyProtectedMember
    def _serialize_(self, _ser_: Scalar_1_0._SerializerTypeVar_) -> None:
        assert _ser_.current_bit_length % 8 == 0, 'Serializer is not aligned'
        _base_offset_ = _ser_.current_bit_length
        _ser_.pad_to_alignment(8)
        self.timestamp._serialize_(_ser_)
        assert _ser_.current_bit_length % 8 == 0, 'Nested object alignment error'
        if _np_.isfinite(self.cubic_meter):
            if self.cubic_meter > 340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(340282346638528859811704183484516925440.0)
            elif self.cubic_meter < -340282346638528859811704183484516925440.0:
                _ser_.add_aligned_f32(-340282346638528859811704183484516925440.0)
            else:
                _ser_.add_aligned_f32(self.cubic_meter)
        else:
            _ser_.add_aligned_f32(self.cubic_meter)
        _ser_.pad_to_alignment(8)
        assert 88 <= (_ser_.current_bit_length - _base_offset_) <= 88, \
            'Bad serialization of uavcan.si.sample.volume.Scalar.1.0'

    # noinspection PyProtectedMember
    @staticmethod
    def _deserialize_(_des_: Scalar_1_0._DeserializerTypeVar_) -> Scalar_1_0:
        assert _des_.consumed_bit_length % 8 == 0, 'Deserializer is not aligned'
        _base_offset_ = _des_.consumed_bit_length
        # Temporary _f0_ holds the value of "timestamp"
        _des_.pad_to_alignment(8)
        _f0_ = uavcan.time.SynchronizedTimestamp_1_0._deserialize_(_des_)
        assert _des_.consumed_bit_length % 8 == 0, 'Nested object alignment error'
        # Temporary _f1_ holds the value of "cubic_meter"
        _f1_ = _des_.fetch_aligned_f32()
        self = Scalar_1_0(
            timestamp=_f0_,
            cubic_meter=_f1_)
        _des_.pad_to_alignment(8)
        assert 88 <= (_des_.consumed_bit_length - _base_offset_) <= 88, \
            'Bad deserialization of uavcan.si.sample.volume.Scalar.1.0'
        assert isinstance(self, Scalar_1_0)
        return self

    def __repr__(self) -> str:
        _o_0_ = ', '.join([
            'timestamp=%s' % self.timestamp,
            'cubic_meter=%s' % self.cubic_meter,
        ])
        return f'uavcan.si.sample.volume.Scalar.1.0({_o_0_})'

    _EXTENT_BYTES_ = 11

    _MODEL_: _pydsdl_.StructureType = _dsdl_.CompositeObject._restore_constant_(
        'ABzY8L4#Cb0{^vFTW{UQ5teMry7?N}j^iZGI!!F8wRm(p@^RX<b(FdZHkJ)v5}`%QF3Hu|g-I^EyOeZ{7Hu9{SO9?#2m|CN<R|2@'
        'Xz~!CK%esyg8qU$W`<lINsj$k1M)ZAot>GT>z=<K`|QJ$BlW-HwQLZXDE55AwPdk;%z~JEeyEa68EJV{oV;&!9@<><2ZM}PpH}l9'
        'SAVVMiZMTB3G83a*>=cM&q&X(B!ko2D$Wz`-49vJbX83F+gux|(n^dJ;~zTu(~6GLk$+YnSH-l?tkp8eEjQI4K=gBr8gf;|*e%K9'
        'Xy2GAKVp{o7A+J<nnf{ITyeHpiS`WAP-vCP$2@uf3&w)El^7S3ttH|FXcuSP@tNn@k!hJoE4RUpnTM&7{gg-Vr<V7*KJ21tKakds'
        'dD^$4qCK!OWXAf5ionWOiVJsJL3qqthrQdlg|7KWb+0PU`CwxjF&!Ngw3i2Pwdq8LS{WXyG^&bYex$-`^M6N1Mji-G(mV;cCTfcu'
        ';4;JtW{F_ioMg-x9uXtckQ1X4PM8K2n&|;a;4`&ErodlwT5k%4x^)n$wCuz7ob<SNt>!`plYkjMPoyCc-;&@Hl5xGjvMiP%vk-HS'
        'pqMb%8s!X+pr+jLDF_q^IMMviIm8BzZ)uh6OE<&t)xt;uhH-t37|v^^P=Q>N!9``-hgH2T;cm4lverHYw*cd|S)6mU(khbjZFCd-'
        'w-u|M#=hZxcWnV&LUv>XcJh#cjc-j&5wbv*|JYqS>{(!EfyymeUhZ|tfHQ5bksTpJfm=`%sU3LaCRtmpWga*ScIS{gn(U}NjzAG;'
        'AS6#y9&%%tmhqr50TO{oYlhZ>+u#^jixKI9Rx4C)kgHY?+ffc82m@^(nD0vPS85@TNvNff#%nIK9z!n3aAE!C2ANBhCAZ$4Cy)s#'
        '_)>$ukZDMYJVSq7C&2)U6g6gS5Gz*47y<>Iz^e^^(1wa6Xnr4<jbL$%5yo`u$9$n?Z&YmYeMco67MdKj!#F@v%vwwf^nu3R6aquQ'
        'iN>p-5Ka{n>ng=EvBSC(GvczNuF#%%UA#d@u%5(hQ##`hH|WNlk2WeXUtIki*Xn82b-qE|&>N3ZwUc^Paon#Bs)|?JroeYINH}a}'
        'hg!nKy*fWx+}b0$#Uxxg#8m_Pw;T=o#pq&%mYE<AcrkOJ5BkBN>92T;IdMs>h=m*)O2k1aloOAtz2cO=C3kt`W1xH)RU5@w->6)N'
        '95!O^XAIg!@wbkE%Iz2#L*{fI=K<U87?!DiXG`j2hiTriO2wuFYAr;_Z<=N&%LAxfU-Nz*qr&|bYdVev9o2beU-g!}MX%w4F6j$q'
        'z#6Q3-&JO{2j2hBMpNl1nV@7$6DWM8p$(vSF=3&a8C0s>QTowBT?*!a#yVKFN=Oka4wV)NfKk*Ge_i|gdf-FIzJTHacd7(BTjUgD'
        'q6P{iL0f9uZ(V%bz@zkn$#^KY<bec-$?%AK*o1=^0(`Yiko}$wm$pxTSH+2Ur2U}&zR!o*TO9RORu$xVLd+lu6vPF*dYdQ8b;CPQ'
        'hRiCxKYNb*p@6!t#NFcbT^3<e{1KCQh`Sqk40C$$^seZBQq9p`X#$wwStFsM6L|plOk|4l3<$Q1#5m40$PyGvNAcW9Nsl-@ig=`?'
        '$K3ZA;%G^ayY+FmKH+fEtxq8yFX^=7KY=(=(vyhCN_xuipGKT6=^3|w7ICbkFE}|fh%c1%9O9Xho<}@Y(hG<uO8O$=R7o$o^DjBQ'
        'mz<uLot#&kzE=@nF6m{&OC@~`@uiXy#ET`pg7{)dUq`%9(w`unFX<bI=Sun};!H`eI=f~O&z5w~**A}Px}-mKcK!_UWJ#|%dl%e&'
        'J!f|Zak8X~&i*CD@scjPd#pHrth)QuaXnhnHFvM;&c8i(zZ*^5>01te?(i25-*)&*hre?8YlrVS+;k`$?mB$p@N<V>IQ-J#Hx9pb'
        '_?^S=8@xR+>WGUiG1n5kmUyovHd{ip#BNJGX^GEU;)|B}vL(K0iEmrtyO#Lg5ji~TU=+Xr!Jh8c0_^B8Y9{UeLvy|u!HG3|Ucw7-'
        '@)pccd+5;!Ba6VuS{AcUKybqP@OsJdz4&%9yRy2t+*@8*U0Yk}b(ed+?v38k()GpFrQXVFZ?(I$c4N7_y4sAC=8+iY0krUh!%G1S'
        '5MRNV5jRoGzr|VcU-5M=*7wA_8{#*`U;ckn!pKhZ%b?TzGUznF3=WP6@!LH#PrNTaXqwL*ac|h8J{nT@4)m?_F!yl~rq67E#bnd}'
        'VC3LWif2l@FMK)*e)<zU5*Yjip!Z)Ju<-i>4Uj+s<OZ2GfoXG}$;V#!qh*Y{_XE_@tE^!S000'
    )
    assert isinstance(_MODEL_, _pydsdl_.StructureType)
