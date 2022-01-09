/*


Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package controllers

import (
	// Core GoLang contexts
	"context"
	"time"

	// 3rd party and SIG contexts
	"github.com/go-logr/logr"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"

	// metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime"

	// "k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"

	// "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	// "sigs.k8s.io/controller-runtime/pkg/reconcile"
	// "k8s.io/client-go/tools/record"

	// Local Operator contexts
	cnatv1alpha1 "cnat/api/v1alpha1"
	"cnat/pkg/schedule"
	"cnat/pkg/spawn"
)

// AtReconciler reconciles a At object
type AtReconciler struct {
	client.Client
	Log    logr.Logger
	Scheme *runtime.Scheme
	// Recorder record.EventRecorder
}

// +kubebuilder:rbac:groups=cnat.awkshwayrd.dev,resources=ats,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=cnat.awkshwayrd.dev,resources=ats/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps,resources=deployments/status,verbs=get;update;patch
func (r *AtReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	ctx := context.Background()
	reqLogger := r.Log.WithValues("at", req.NamespacedName)

	reqLogger.Info("Reconciling on At resource")
	instance := &cnatv1alpha1.At{}
	err := r.Get(ctx, req.NamespacedName, instance)
	if err != nil {
		//when Reconcile got called for object deletion we tried to get the object and got an error
		//simply return, nothing else to do
		if errors.IsNotFound(err) {
			reqLogger.Info("object already deleted")
			return ctrl.Result{}, nil
		}
	}

	if instance.Status.Phase == "" {
		instance.Status.Phase = cnatv1alpha1.PhasePending
	}

	// your logic here
	switch instance.Status.Phase {
	case cnatv1alpha1.PhasePending:
		reqLogger.Info("Phase: PENDING")

		diff, err := schedule.TimeUntilSchedule(instance.Spec.Schedule)
		if err != nil {
			reqLogger.Error(err, "error parsing schedule")
			return ctrl.Result{}, err
		}

		if diff < 0 {
			//not yet time to execute the command
			//requeue the request
			reqLogger.Info("not yet time!")
			return ctrl.Result{RequeueAfter: diff * time.Second}, nil
		}

		reqLogger.Info("It's time!", "Ready to execute", instance.Spec.Command)

		//change the state
		instance.Status.Phase = cnatv1alpha1.PhaseRunning

	case cnatv1alpha1.PhaseRunning:
		reqLogger.Info("Phase: RUNNING")
		pod := spawn.NewPodForCR(instance)
		err := ctrl.SetControllerReference(instance, pod, r.Scheme)
		if err != nil {
			return ctrl.Result{}, err
		}
		query := &corev1.Pod{}
		err = r.Get(ctx, req.NamespacedName, query)
		if err != nil && errors.IsNotFound(err) {
			//pod does not exist, create one now
			err := r.Create(ctx, pod)
			if err != nil {
				return ctrl.Result{}, err
			}
			reqLogger.Info("Successfully created a pod", "name", pod.Name)
			return ctrl.Result{}, nil
		} else if err != nil {
			reqLogger.Error(err, "Cannot create a pod")
			return ctrl.Result{}, err
		} else if query.Status.Phase == corev1.PodFailed ||
			query.Status.Phase == corev1.PodSucceeded {
			//pod has already finished or errored out
			reqLogger.Info("Container terminated")
			instance.Status.Phase = cnatv1alpha1.PhaseDone
		} else {
			return ctrl.Result{}, nil
		}

	case cnatv1alpha1.PhaseDone:
		reqLogger.Info("Phase: DONE")
		return ctrl.Result{}, nil
	default:
		reqLogger.Info("Unknown Phase")
		return ctrl.Result{}, nil
	}
	// Propogate the changes to the CR in etcd
	err = r.Status().Update(ctx, instance)
	if err != nil {
		return ctrl.Result{}, err
	}

	return ctrl.Result{}, nil
}

func (r *AtReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&cnatv1alpha1.At{}).
		Owns(&cnatv1alpha1.At{}).
		Owns(&corev1.Pod{}).
		Complete(r)
}

/*
func (r *AtReconciler) Reconcile(req ctrl.Request) (ctrl.Result, error) {
	_ = context.Background()
	logger := r.Log.WithValues("namespace",
	req.NamespacedName, "at", req.Name)
	logger.Info("== Reconciling At")

	// your logic here
	  // Fetch the At instance
  instance := &cnatv1alpha1.At{}
  err := r.Get(context.TODO(), req.NamespacedName, instance)
  if err != nil {
    if errors.IsNotFound(err) {
      // Request object not found, could have been deleted after reconcile request - return and don't requeue:
      return reconcile.Result{}, nil
    }
    // Error reading the object - requeue the request:
    return reconcile.Result{}, err
  }

    // If no phase set, default to pending (the initial phase):
  if instance.Status.Phase == "" {
    instance.Status.Phase = cnatv1alpha1.PhasePending
  }

    // Make the main case distinction: implementing
  // the state diagram PENDING -> RUNNING -> DONE
  switch instance.Status.Phase {
    case cnatv1alpha1.PhasePending:
      logger.Info("Phase: PENDING")
	  r.Recorder.Event(instance, "Normal", "PhaseChange", cnatv1alpha1.PhasePending)
      // As long as we haven't executed the command yet, we need to check if it's time already to act
      logger.Info("Checking schedule", "Target", instance.Spec.Schedule)
      // Check if it's already time to execute the command with a tolerance of 2 seconds:
      d, err := timeUntilSchedule(instance.Spec.Schedule)
      if err != nil {
        logger.Error(err, "Schedule parsing failure")
        // Error reading schedule. Wait until it is fixed.
        return reconcile.Result{}, err
      }
      logger.Info("Schedule parsing done", "Result", fmt.Sprintf("diff=%v", d))
      if d > 0 {
        // Not yet time to execute command, wait until the scheduled time
        return reconcile.Result{RequeueAfter: d}, nil
      }
      logger.Info("It's time!", "Ready to execute", instance.Spec.Command)
      instance.Status.Phase = cnatv1alpha1.PhaseRunning

    case cnatv1alpha1.PhaseRunning:
      logger.Info("Phase: RUNNING")
	  r.Recorder.Event(instance, "Running", "PhaseChange", cnatv1alpha1.PhaseRunning)
      pod := newPodForCR(instance)
      // Set At instance as the owner and controller
      if err := controllerutil.SetControllerReference(instance, pod, r.Scheme); err != nil {
        // requeue with error
        return reconcile.Result{}, err
      }
      found := &corev1.Pod{}
      err = r.Get(context.TODO(), types.NamespacedName{Name: pod.Name, Namespace: pod.Namespace}, found)
      // Try to see if the Pod already exists and if not
      // (which we expect) then create a one-shot Pod as per spec:
      if err != nil && errors.IsNotFound(err) {
        err = r.Create(context.TODO(), pod)
        if err != nil {
          // requeue with error
          return reconcile.Result{}, err
        }
        logger.Info("Pod launched", "name", pod.Name)
      } else if err != nil {
        // requeue with error
        return reconcile.Result{}, err
      } else if found.Status.Phase == corev1.PodFailed || found.Status.Phase == corev1.PodSucceeded {
        logger.Info("Container terminated", "reason", found.Status.Reason, "message", found.Status.Message)
        instance.Status.Phase = cnatv1alpha1.PhaseDone
      } else {
        // don't requeue because it will happen automatically when the Pod status changes
        return reconcile.Result{}, nil
      }

    case cnatv1alpha1.PhaseDone:
      logger.Info("Phase: DONE")
	  r.Recorder.Event(instance, "Done", "PhaseChange", cnatv1alpha1.PhaseDone)
      return reconcile.Result{}, nil

    default:
      logger.Info("NOP")
      return reconcile.Result{}, nil
  }

    // Update the At instance, setting the status to the respective phase:
  err = r.Status().Update(context.TODO(), instance)
  if err != nil {
    return reconcile.Result{}, err
  }

	return ctrl.Result{}, nil
}
*/
