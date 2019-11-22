#
# This is module that will handing all routines related to clustering
#


# Now, let's try out a real clustering algorithm - DBSCAN
from enum import Enum

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from sklearn.cluster import DBSCAN
from itertools import groupby
from functools import reduce

from Point import Point
from Trial import Trial
from VisualizationUtility import get_color_i_of_n

class DataTypeCluster(Enum):
    GAZE_POINTS = 0
    FIXATIONS = 1
    FIXATIONS_TOBII = 2

class Clustering:
    """
    This class handles every aspect of performing a clustering. The class is mostly written to manage any general
    clustering, though it has numerous hooks specifically for managing eyetracking data

    """
    def __init__(self, cluster_data_type: DataTypeCluster, start_ts=None, end_ts=None):
        """
        Set up the clustering object.
        :param cluster_data_type: DataTypeCluster enumerated type
        :param start_ts: Limit data to cluster by setting this to a timestamp (None to use all)
        :param end_ts: Limit data to cluster by setting this to a timestamp (None to use all)
        """
        self.cluster = None
        self.n_clusters = 0
        self.n_outliers = 0
        self.trials = []
        self.X_obj_list = []
        self.X_as_np_array = None
        self._data_type = cluster_data_type
        self._start_ts = start_ts
        self._end_ts = end_ts
        self.labels_for_X_with_minus1 = []
        self.labels_for_X = []
        self.clusters_for_trials = []
        self.unique_cluster_labels = None
        self.map_cluster_label_to_cluster = {}

    def __repr__(self):
        if type(self.cluster) is DBSCAN:
            s = "n_clusters = {}\n".format(self.n_clusters)
            s += "n_outliers = {}\n".format(self.n_outliers)
            s += "len(self.trials) = {}\n".format(len(self.trials))
            s += "len(self.X_obj_list) = {}\n".format(len(self.X_obj_list))
            s += "len(self.X_as_np_array) = {}\n".format(len(self.X_as_np_array))
            s += "len(self.labels_for_X) = {}\n".format(len(self.labels_for_X))
            s += "set(self.labels_for_X) = {}\n".format(set(self.labels_for_X))
            s += "unique_cluster_labels = {}".format(self.unique_cluster_labels)
            s += "len(set(self.cluster.labels_) = {}\n".format(len(set(self.cluster.labels_)))
            s += "type(self.cluster._labels) = {}\n".format(type(self.cluster.labels_))
            s += "core_sample_indices_ = Indices of core samples.\n"
            s += "self.cluster.core_sample_indices_ = {}\n".format(self.cluster.core_sample_indices_)
            s += "len(self.cluster.core_sample_indices_) = {}\n".format(len(self.cluster.core_sample_indices_))
            s += "components_ = Copy of each core sample found by training.\n"
            s += str(self.cluster.components_)
            s += "\nlen(self.cluster.components_) = {}\n".format(len(self.cluster.components_))
            # s += "\ncluster_for_trials = {}\n".format(self.clusters_for_trials)

            return s

    # def set_data_type(self, data_type):
    #     # If there was a type already set, then we must reset everything
    #     if self._data_type is not None:
    #         self.__init__()
    #
    #     self._data_type = data_type

    def add_data_for_clustering(self, data, use_ts=False, use_dur=False):
        """
        This method is called to add data to be clustered

        :param data: The data to be added. This can be different types, depending on the data that is going to be clustered. This can be a Trial object, and the data pulled from the trail depends on the data type being clustered
        :param use_ts: Use the time stamp when adding data points? Works for fixations only.
        :param use_dur: Use the duration for each fixation? works for fixations only.
        :param start_ts: start timestamp to limit data to start using for clustering (None uses first point)
        :param end_ts: ending timestamp to limit data to stop using for clustering (None uses to last point)
        :return: Nothing
        """

        trial = None
        if type(data) is Trial:
            self.trials.append(data)
            trial = data

        # grab the nparray of fixation coordinates.
        if self._data_type is DataTypeCluster.FIXATIONS_TOBII:
            # get the corresponding fixations
            X_obj = trial.get_fixations_obj_list(start_ts=self._start_ts, end_ts=self._end_ts, isTobii=True)
            X = trial.get_np_fixation_data(use_coord=True,use_dur=use_dur, use_ts=use_ts, start_ts=self._start_ts, end_ts=self._end_ts, isTobii=True)

        elif self._data_type is DataTypeCluster.GAZE_POINTS:
            X_obj = trial.get_sample_list(start_ts=self._start_ts, end_ts=self._end_ts)
            X = trial.get_np_gaze_point_coordinates(start_ts=self._start_ts, end_ts=self._end_ts)

        if len(X_obj) > 0:
            self.X_obj_list.extend(X_obj)
            if self.X_as_np_array is None:
                self.X_as_np_array = X
            elif len(X) > 0:
                self.X_as_np_array = np.append(self.X_as_np_array, X, axis=0)

    def run_DBSCAN(self, eps, min_samples):
        """
        Run the DBSCAN clustering algorithm

        :param eps: radius of data to be considered
        :param min_samples: minimum number of samples that must fall within a radius
        :return: Nothing
        """
        # if self._data_type is None:
        #     raise Exception("Set data type first!")

        if self.X_as_np_array is None:
            if not self.trials:
                raise Exception("No trials added!")
            else:
                raise Exception('No data extracted from trials')

        self.cluster = DBSCAN(eps = eps, min_samples=min_samples).fit(self.X_as_np_array)

        # Number of clusters, ignoring noise if present.
        self.n_clusters = len(set(self.cluster.labels_)) - (1 if -1 in self.cluster.labels_ else 0)

        # Set up a mask of only the core samples
        #core_samples_mask = np.zeros_like(self.cluster.labels_, dtype=bool)
        #core_samples_mask[self.cluster.core_sample_indices_] = True

        # Copy the reference to the list of labels with the -1 indicator for outliers
        self.labels_for_X_with_minus1 = self.cluster.labels_

        # Gather the set of cluster labels
        self.unique_cluster_labels = set(self.cluster.labels_)

        # Make a copy of the labels so we can create a list with singleton / outliers being assigned cluster ids. This
        # is important for the itemset mining
        self.labels_for_X = list(self.cluster.labels_)

        # Remove all outliers to be singleton clusters with their own label (instead of -1)
        # AND create new Cluster objects to help us analyze what is in each cluster
        for i in range(len(self.X_obj_list)):
            cluster_label = self.labels_for_X[i]
            # If this was not clustered, then it will be a singleton cluster
            if cluster_label < 0:
                cluster_label = self.n_clusters + self.n_outliers
                self.labels_for_X[i] = cluster_label
                self.n_outliers += 1

            # If we have not come across this id yet, then initialize a new Cluster object
            if cluster_label not in self.map_cluster_label_to_cluster:
                self.map_cluster_label_to_cluster[cluster_label] = Cluster(cluster_label)

            # Add this object to the Cluster
            self.map_cluster_label_to_cluster[cluster_label].add_object_to_cluster(self.X_obj_list[i])

        # Finally, go back through the data and assign the cluster label to each object that was clustered
        i_cluster_label = 0
        for i in range(len(self.trials)):
            t = self.trials[i]
            X_cluster_list = []

            # Iterate through the original fixation sequence, and replace with the updated sequence
            if self._data_type is DataTypeCluster.FIXATIONS_TOBII:
                for fix in t.get_fixations_obj_list(start_ts=self._start_ts,end_ts=self._end_ts,isTobii=True):
                    cluster_label = self.labels_for_X[i_cluster_label]
                    X_cluster_list.append(self.map_cluster_label_to_cluster[cluster_label])
                    i_cluster_label += 1

            elif self._data_type is DataTypeCluster.GAZE_POINTS:
                for sample in t.get_sample_list(start_ts=self._start_ts, end_ts=self._end_ts):
                    cluster_label = self.labels_for_X[i_cluster_label]
                    X_cluster_list.append(self.map_cluster_label_to_cluster[cluster_label])
                    i_cluster_label += 1

            self.clusters_for_trials.append(X_cluster_list)

    def print_all_clusters(self):
        for cluster_label in self.map_cluster_label_to_cluster.keys():
            print("[{}] = {}".format(cluster_label, self.map_cluster_label_to_cluster[cluster_label]))

    def plot_clusters(self, ax: Axes, **kwargs):
        cluster_label_colors = [plt.cm.nipy_spectral(each)
                                for each in np.linspace(0, 1, len(self.unique_cluster_labels))]

        for k, col in zip(self.unique_cluster_labels, cluster_label_colors):
            if k == -1:
                col = [0, 0, 0, 1]
                size = 3
            else:
                size = 6

            # Set up a class membership mask belonging to cluster k
            class_member_mask = (self.cluster.labels_ == k)

            # Identify the points in cluster k
            xy = self.X_as_np_array[class_member_mask]

            ax.plot(xy[:, 0], xy[:, 1], marker='o', markerfacecolor=tuple(col), markeredgecolor='k',
                    markersize=size, linestyle="None", label=str(k), **kwargs)


    def plot_clusters_2(self, ax: Axes, labelcolor='white', labelsize=10, **kwargs):
        """
        This methods will plot all of the clusters in one color, with a number at the centroid
        position of each cluster.
        
        :param ax: The Axes object to plot to
        :param labelcolor: Def: 'white'. The color of the font passed to the centroid label plotted.
        :param labelsize: Def: 10. fontsize passed to the centroid label plotted
        :param kwargs: Currently unused
        :return: Nothing
        """
        for cluster_id in self.map_cluster_label_to_cluster:
            cluster = self.map_cluster_label_to_cluster[cluster_id]
            if len(cluster.objects) > 1:
                cluster.plot_cluster(ax, s=10, color='red')
                cluster.plot_centroid(ax, plotLabel=True, color=labelcolor, fontsize=labelsize, weight="bold")
            else:
                cluster.plot_cluster(ax, s=1, c='black')

    def plot_clusters_labels(self, ax: Axes, fontsize=12, color='white', weight='bold', **kwargs):
        """
        This method plots only cluster labels as identifying numbers at the centroid position of each cluster. Only
        clusters that have membership > 1 are plotted. All others are ignored

        :param ax: The Axes object to plot to
        :param fontsize: Fontsize to use for each label
        :param color: color to use for each label
        :param weight: weight to use for each label
        :param kwargs:
        :return: Nothing
        """
        for cluster_id in self.map_cluster_label_to_cluster:
            cluster = self.map_cluster_label_to_cluster[cluster_id]
            if len(cluster.objects) > 1:
                cluster.plot_centroid(ax, plotLabel=True, color=color, weight=weight, fontsize=fontsize)

    def plot_clustered_scanpath_by_trial(self, ax: Axes, i_trial_added = None, min_cluster_size=1, index_of_color = None,
                                         show_seq_label = False, label_type="cluster_id", labelcolor='white', labelweight='bold', fontsize=12,  **kwargs):
        """
        Plot a scanpath based on its clusters.
        :param ax: Axes to plot on
        :param i_trial_added: The index of the trial, or just plot all of them if i_trial_added is None
        :param min_cluster_size: Plot only clusters that meet or exceed min_cluster_size
        :param index_of_color: Index of the colormap to use from the VisualizatonUtility package, or none if printing all scanpaths
        :param show_seq_label: Show a sequence number on the path plotted?
        :param label_type: "cluster_id" - cluster label, or "sequence_id" - number in sequence
        :param labelcolor: Color to show on the label in the scanpath
        :param labelweight: Width of the font to show for the label in the scanpath
        :param fontsize: The fontsize to use if we're plotting a sequence label
        :param kwargs: Passed to ax.plot
        :return:
        """
        i_trial = 0
        if i_trial_added:
           i_trial = i_trial_added

        while i_trial < len(self.trials):
            # clustered_list = self.clusters_for_trials[i_trial]
            clustered_list = [c for c in self.clusters_for_trials[i_trial] if len(c.objects) >= min_cluster_size]
            centroids = [clust.centroid for clust in clustered_list]

            # Plot a point label...
            if show_seq_label:
                for i in range(len(centroids)):
                    p = centroids[i]
                    if label_type == "cluster_id":
                        s_label = str(clustered_list[i].clust_id)
                    elif label_type == "sequence_id":
                        s_label = str(i)
                    else:
                        raise ValueError("Bad value for parameter label_type: {}".format(label_type))

                    ax.text(p.val[0], p.val[1], s_label, va='center', ha='center', color=labelcolor,
                            weight=labelweight, fontsize=fontsize)

            if index_of_color != None:
                # kwargs["color"]  = [get_color_i_of_n(index_of_color)]*len(path.points)
                kwargs["color"] = get_color_i_of_n(index_of_color)

            ax.plot([p.val[0] for p in centroids], [p.val[1] for p in centroids],
                    lineStyle="-",**kwargs)

            if i_trial_added:
                break
            i_trial += 1

    def get_cluster_label_sequence_for_trial(self, i_trial_added, min_cluster_size, compress_adj=False) -> pd.DataFrame:
        """
        Return a DataFrame of cluster labels, duration on the cluster, and time between clusters for a trial

        NOTE: Only supports Tobii Fixations at the moment!

        :param i_trial_added: Index of the trial added for clustering to gather info for
        :param min_cluster_size: Minimum number of fixations in the cluster
        :param compress_adj: True? Then aggregate adjacent fixations into one
        :return: pandas DataFrame { label : [], num_obj, ts:[], dur : [], gap : [] }
        """

        cluster_info = []

        if self._data_type == DataTypeCluster.FIXATIONS_TOBII:
            obj_list = self.trials[i_trial_added].get_fixations_obj_list(start_ts=self._start_ts, end_ts=self._end_ts)
            for i in range(len(obj_list)):
                # cluster_info.append(
                #     [self.clusters_for_trials[i_trial_added][i].clust_id,         # 0 = cluster label
                #      len(self.clusters_for_trials[i_trial_added][i].objects),     # 1 = number of objects in cluster
                #      self.trials[i_trial_added].fixations_Tobii[i].start_ts,      # 2 = start time for cluster
                #      self.trials[i_trial_added].fixations_Tobii[i].duration,      # 3 = length of time on cluster
                #      0]                                                         # 4 = gap time
                # )
                cluster_info.append(
                    [self.clusters_for_trials[i_trial_added][i].clust_id,  # 0 = cluster label
                     len(self.clusters_for_trials[i_trial_added][i].objects),  # 1 = number of objects in cluster
                     obj_list[i].start_ts,  # 2 = start time for cluster
                     obj_list[i].duration,  # 3 = length of time on cluster
                     0]  # 4 = gap time
                )

                # Compute gap of previous item
                if i > 0:
                    # gap = cur ts - (last ts + duration of last)
                    gap = cluster_info[-1][2] - (cluster_info[-2][2] + cluster_info[-2][3])
                    cluster_info[-2][4] = gap

        elif self._data_type == DataTypeCluster.GAZE_POINTS:
            obj_list = self.trials[i_trial_added].get_sample_list(start_ts=self._start_ts, end_ts=self._end_ts)
            for i in range(len(obj_list)):
                cluster_info.append(
                    [self.clusters_for_trials[i_trial_added][i].clust_id,  # 0= Cluster label
                     len(self.clusters_for_trials[i_trial_added][i].objects),  # 1 = number of objects in cluster
                     obj_list[i].ts,  # 2 = start time for cluster
                     1,  # 3 = These are gaze points, no time
                     0]                                                     # 4 = gap time, 0
                )

        else:
            raise NotImplementedError

        # num_fixations = len(self.clusters_for_trials[i_trial_added])


        # Let's filter out those clusters that do not meet min_cluster_size criteria
        new_cluster_info = []
        for is_clust_size_good, group in groupby(cluster_info, lambda x : x[1] >= min_cluster_size):
            # Cluster good? Then just append all the items
            if is_clust_size_good:
                new_cluster_info.extend(list(group))
            # No good? Then accumulate all the durations and gaps, and add them to the previous gap
            elif len(new_cluster_info) > 0:
                gap_to_add = sum([x[3] + x[4] for x in group])
                new_cluster_info[-1][4] += gap_to_add
        cluster_info = new_cluster_info

        # Now, let's compress adjacent clusters that are identical
        if compress_adj:
            new_cluster_info = []
            for clust_id, group in groupby(cluster_info, lambda x : x[0]):
                list_group = list(group)
                if len(list_group) == 1:
                    new_cluster_info.extend(list_group)
                else:
                    # Sum all durations and gaps for all but last one
                    new_duration = sum([x[3] + x[4] for x in list_group[:-1]])
                    list_group[0][3] = list_group[-1][3] + new_duration
                    # New gap is the gap of last item
                    list_group[0][4] = list_group[-1][4]
                    new_cluster_info.append(list_group[0])
            cluster_info = new_cluster_info

        # Eliminate clusters without min_cluster_size
#        cluster_label_sequence = [cluster.clust_id for cluster in self.clusters_for_trials[i_trial_added]
#                                  if len(cluster.objects) >= min_cluster_size]

        # Do we need to remove adjacent items that are identical?
#        if compress_adj:
#            cluster_label_sequence = [k for k, g in groupby(cluster_label_sequence)]

#        return cluster_label_sequence

        return pd.DataFrame(
#            { "trial_id" : [i_trial_added]*len(cluster_info),
            { "subject_id": [str(self.trials[i_trial_added].participantName)] * len(cluster_info),
              "label" : [x[0] for x in cluster_info],
              "num_obj" : [x[1] for x in cluster_info],
              "ts" : [x[2] for x in cluster_info],
              "dur" : [x[3] for x in cluster_info],
              "gap" : [x[4] for x in cluster_info]
            }, columns=['subject_id', 'label', 'num_obj', 'ts', 'dur', 'gap'])

class Cluster:

    def __init__(self, clust_id: int):

        # The list of objects in this cluster
        self.objects = []
        self.clust_id = clust_id
        self.centroid = None
        self.point = None       # This is the same as centroid, used for convenience to mirror Fixation

    def __str__(self):
        s = "Cluster: clust_id = {}, # of fixations = {}, centroid = {}".format(
            self.clust_id, len(self.objects), str(self.centroid))
        if (len(self.objects) > 0):
            s += " type = {}".format(type(self.objects[0]))
        return s

    # TODO - This is hard coded to work only with points! Objects can have more than just point data!!!

    def add_object_to_cluster(self, object):
        self.objects.append(object)
        total_point = Point(0,0)
        #print("add_object_to_cluster id {}: {}".format(self.clust_id, str(f)))
        for object in self.objects:
            total_point = object.point + total_point
        total_point /= len(self.objects)
        self.point = self.centroid = total_point

    def get_centroid_point(self):
        return self.centroid

    def plot_cluster(self, ax: Axes, **kwargs):
        """
        Plot the cluster of points to a matplotlib Axes object

        :param ax:
        :param kwargs:
        :return:
        """
        ax.scatter([f.point.val[0] for f in self.objects],
                   [f.point.val[1] for f in self.objects],
                   **kwargs)

    def plot_centroid(self, ax: Axes, plotLabel=True, **kwargs):
        """
        Plot the centroid to a matplotlib Axes object. You can pass standard parameters through 
        kwargs, including `fontsize` and `color` parameters.

        :param ax:
        :param kwargs:
        :return:
        """

        if plotLabel:
            ax.text(self.centroid.val[0], self.centroid.val[1], str(self.clust_id), va='center', ha='center', **kwargs)
        else:
            ax.plot(self.centroid.val[0], self.centroid.val[1], **kwargs)


if __name__ == "__main__":
    from StudyManager import StudyManager
    from FileProcessor import FieldId

    # Set up default directories
    experimentDir = '/Users/brk009/Google Drive/Grants/201802 Simons Explorer/MAP Trajectory Data/MAP TSV/'
    field_config = [FieldId.PROJECT_NAME,
                    FieldId.TEST_NAME,
                    FieldId.PARTICIPANT_NAME,
                    FieldId.MEDIA_NAME,
                    FieldId.MEDIA_POS_X,
                    FieldId.MEDIA_POS_Y,
                    FieldId.TIMESTAMP,
                    FieldId.EVENT_CODES,
                    FieldId.FIXATION_X,
                    FieldId.FIXATION_Y,
                    FieldId.GAZE_POINT_X,
                    FieldId.GAZE_POINT_Y,
                    FieldId.EYE_LEFT_POS_X,
                    FieldId.EYE_LEFT_POS_Y]

    imageLibDir = '/Users/brk009/Google Drive/Grants/201802 Simons Explorer/MAP Trajectory Data/Stimuli/'

    sm = StudyManager(min_frac_sample_good=0.5,min_num_fixations=5)
    sm.process_run_files(experimentDir, field_config)
    sm.process_stimulus_files(stimulus_dir=imageLibDir,ext=".bmp")

    tests = sm.get_test_names()
    runs = sm.get_runs_for(test_name=tests[0])
    stimulus = sm.get_stimulus_names()[3]
    trials = sm.get_trials_for_stimulus(stimulus)
    n_trials = 40
    trials = trials[:n_trials]

    cluster = Clustering(DataTypeCluster.FIXATIONS_TOBII)
    for t in trials:
        cluster.add_data_for_clustering(t)

    cluster.run_DBSCAN(eps=30, min_samples=10)
    print(repr(cluster))

    fig = plt.figure()
    ax = fig.add_subplot(121)
    cluster.plot_clusters(ax)
    ax.legend(bbox_to_anchor=(1.5,1.1),loc=1, ncol=2, title="Cluster id")
    ax.imshow(sm.get_stimulus_mpimg(stimulus_name=stimulus), origin='upper')
    ax.set_ylim(750,0)
    #plt.ylim([0, 1000])
    #plt.xlim([0, 1200])
    plt.grid()
    #plt.show()

    #fig = plt.figure()
    ax = fig.add_subplot(122)
    ax.imshow(sm.get_stimulus_mpimg(stimulus_name=stimulus), origin='upper')
    cluster.plot_clusters_2(ax)
    plt.show()

    df = pd.DataFrame()

    for i in range(n_trials):
        df = df.append(cluster.get_cluster_label_sequence_for_trial(i,1))

    print(df)

    for i in range(n_trials):
        df = df.append(cluster.get_cluster_label_sequence_for_trial(i,2,
                                                           compress_adj=False))

    for i in range(n_trials):
        df = df.append(cluster.get_cluster_label_sequence_for_trial(i,2,
                                                           compress_adj=True))



    cluster = Clustering(DataTypeCluster.GAZE_POINTS)
    cluster.add_data_for_clustering(trials[0])
    cluster.run_DBSCAN(eps=30, min_samples=5)
    print(repr(cluster))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(sm.get_stimulus_mpimg(stimulus_name=stimulus), origin='upper')

    from VisualizationUtility import plot_fixations_of_trial, init_colormap_over_n
    init_colormap_over_n(1)
    plot_fixations_of_trial(trial=trials[0], ax=ax, index_of_color=0, useTobii=True)
    cluster.plot_clusters(ax)
    plt.show()
