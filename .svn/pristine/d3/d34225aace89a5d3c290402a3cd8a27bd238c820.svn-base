"""Classes for holding parsed data from RTPlan file"""


class BrachyPlan(object):
    def __init__(self, ds):
        self.ds = ds
        self.applicator = self.ds.ApplicationSetupSequence[0][0x300b, 0x100f].value
        self.points = self.get_poi()
        self.channel_numbers = self.get_channel_numbers()
        self.prescription = float(
            ds.FractionGroupSequence[0].ReferencedBrachyApplicationSetupSequence[0].BrachyApplicationSetupDose)
        self.treatment_model = ds.TreatmentMachineSequence[0].TreatmentMachineName
        self.ref_air_kerma_rate = float(ds.SourceSequence[0].ReferenceAirKermaRate)
        self.channels = self.get_channel_dwell_times()
        self.total_number_dwells = sum([len(i) for i in self.channels])
        self.half_life = float(ds.SourceSequence[0].SourceIsotopeHalfLife)
        self.patient_id = ds.PatientID
        self.plan_name = ds.RTPlanLabel

    def get_channel_numbers(self):
        return [int(x.SourceApplicatorID) for x in self.ds.ApplicationSetupSequence[0].ChannelSequence]

    def get_poi(self):
        points = []
        for p in self.ds.DoseReferenceSequence:
            points.append(self.Point(p))
        return points

    def get_channel_dwell_times(self):
        channel_dwells = []
        for c in range(len(self.ds.ApplicationSetupSequence[0].ChannelSequence)):
            total_channel_time = float(self.ds.ApplicationSetupSequence[0].ChannelSequence[c].ChannelTotalTime)
            dwell_weights = []
            dwells_list = []
            number_of_dwells = int(self.ds.ApplicationSetupSequence[0].ChannelSequence[c].NumberOfControlPoints / 2)
            for i in range(0, len(self.ds.ApplicationSetupSequence[0].ChannelSequence[c].BrachyControlPointSequence), 2):
                d1 = float(
                    self.ds.ApplicationSetupSequence[0].ChannelSequence[c].BrachyControlPointSequence[
                        i].CumulativeTimeWeight)
                d2 = float(
                    self.ds.ApplicationSetupSequence[0].ChannelSequence[c].BrachyControlPointSequence[
                        i + 1].CumulativeTimeWeight)
                dwell_weights.append(d2 - d1)
                dwells_list.append(self.ds.ApplicationSetupSequence[0].ChannelSequence[c].BrachyControlPointSequence[
                        i])
            dwell_times = [(total_channel_time / number_of_dwells) * x for x in dwell_weights]
            dwells = []
            for i in range(len(dwells_list)):
                dwells.append(self.Dwell(dwells_list[i],dwell_times[i],dwell_weights[i]))
            channel_dwells.append(dwells)
        return channel_dwells

    class Point(object):
        def __init__(self, ds_sequence):
            self.name = ds_sequence.DoseReferenceDescription
            self.coords = [float(x) for x in ds_sequence.DoseReferencePointCoordinates]
            self.dose = float(ds_sequence.TargetPrescriptionDose)

    class Dwell(object):
        def __init__(self, control_sequence, d_time, d_weight):
            self.coords = [float(x) for x in control_sequence.ControlPoint3DPosition]
            self.time_weight = d_weight
            self.dwell_time = d_time


class PointComparison(object):
    def __init__(self, point_name, omp_dose, pytg43_dose):
        self.point_name = point_name
        self.omp_dose = omp_dose
        self.pytg43_dose = pytg43_dose
        self.abs_difference = omp_dose-pytg43_dose
        self.percentage_difference = 100*((self.omp_dose/self.pytg43_dose)-1)

if __name__ == '__main__':
    print("Ran as script")