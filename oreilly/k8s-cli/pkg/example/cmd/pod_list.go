package cmd

import (
	"fmt"
	"io"    
	apiv1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

    "github.com/codementor/k8s-cli/pkg/example/env"

	"github.com/spf13/cobra"
)

const (
	podListDesc = `List pods.
`
	podListExample = `  kubectl example pod list
`
)

type podListCmd struct {
	// status boolean
	out    io.Writer
}

// newPodListCmd lists pods
func newPodListCmd(out io.Writer) *cobra.Command {

	pkg := &podListCmd{out: out}
	cmd := &cobra.Command{
		Use:     "list",
		Short:   podListDesc,
		Example: podListExample,
		RunE: func(cmd *cobra.Command, args []string) error {
			if err := pkg.run(); err != nil {
				return err
			}
			return nil
		},
	}

	// status flag

	return cmd
}

// newPodList2Cmd lists pods
func newPodList2Cmd(out io.Writer) *cobra.Command {

	pkg := &podListCmd{out: out}
	cmd := &cobra.Command{
		Use:     "list2",
		Short:   podListDesc,
		Example: podListExample,
		RunE: func(cmd *cobra.Command, args []string) error {
			if err := pkg.run2(); err != nil {
				return err
			}
			return nil
		},
	}

	// status flag

	return cmd
}

// run 1st approach at list pods
func (p *podListCmd) run() error {

	// fmt.Printf("add pod list code using direct object references\n")
	// Acquire a kube client and a pods client
	client := env.NewClientSet(&Settings)
	podsClient := client.CoreV1().Pods(apiv1.NamespaceDefault)

	// Query pod clients for a list of pods
	list, err := podsClient.List(metav1.ListOptions{})
	if err != nil {
		return err
	}

	if len(list.Items) == 0 {
		fmt.Printf("No Pods discovered.\n")
		return nil
	}

	for _, item := range list.Items {
		if p.status {
		  fmt.Fprintf(p.out, "pod %v in namespace: %v, status: %v\n", item.Name, item.Namespace, item.Status.Phase)
		} else {
		  fmt.Fprintf(p.out, "Pod %v in Namespace: %v\n", item.Name, item.Namespace)
		}
	}
	return nil
}

// run2 2nd approach at list pods
func (p *podListCmd) run2() error {

	//REST Client approach

	client := env.NewRestClient(&Settings)
	result := &apiv1.PodList{}
	err := client.Get().
		Namespace(apiv1.NamespaceDefault).
		Resource("pods").
		Do().
		Into(result)
	if err != nil {
	  return err
	}
	fmt.Fprintf(p.out, "RESTifarian technique\n")
	if len(result.Items) == 0 {
	  fmt.Printf("no pods discovered\n")
	  return nil
	}
	for _, item := range result.Items {
	  fmt.Fprintf(p.out, "Pod %v in Namespace: %v\n", item.Name, item.Namespace)
	}
   
	return nil
}
